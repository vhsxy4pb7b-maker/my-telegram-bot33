"""消息处理器实现"""
from typing import Dict, Any
from .base import BaseProcessor, ProcessorResult, ProcessorStatus, ProcessorContext
from src.database.models import MessageType
import logging

logger = logging.getLogger(__name__)


class MessageReceiver(BaseProcessor):
    """消息接收处理器 - 准备消息摘要和提取信息"""
    
    def __init__(self):
        super().__init__("message_receiver", "消息接收和预处理")
    
    async def process(self, context: ProcessorContext) -> ProcessorResult:
        """接收消息并生成摘要"""
        try:
            message_content = context.message_data.get("content", "")
            
            # 生成消息摘要（最多500字符）
            if len(message_content) > 500:
                context.message_summary = message_content[:497] + "..."
            else:
                context.message_summary = message_content
            
            # 提取关键信息
            from src.collector.data_collector import DataCollector
            collector = DataCollector(context.db)
            context.extracted_info = collector.extract_info_from_message(message_content)
            
            return ProcessorResult(
                status=ProcessorStatus.SUCCESS,
                message="消息接收成功",
                data={"summary": context.message_summary}
            )
        except Exception as e:
            logger.error(f"Error in message receiver: {str(e)}", exc_info=True)
            return ProcessorResult(
                status=ProcessorStatus.ERROR,
                message=f"消息接收失败: {str(e)}",
                error=e
            )


class UserInfoHandler(BaseProcessor):
    """用户信息处理 - 获取或创建客户"""
    
    def __init__(self):
        super().__init__("user_info_handler", "用户信息处理")
    
    def get_dependencies(self) -> list:
        return ["message_receiver"]
    
    async def process(self, context: ProcessorContext) -> ProcessorResult:
        """获取或创建客户信息"""
        try:
            from src.ai.conversation_manager import ConversationManager
            conversation_manager = ConversationManager(context.db)
            
            sender_id = context.message_data.get("sender_id")
            
            # 尝试获取用户信息
            try:
                platform_user_info = await context.platform_client.get_user_info(sender_id)
                if context.platform_name == "facebook":
                    context.user_info = {
                        "name": platform_user_info.get("name"),
                        "first_name": platform_user_info.get("first_name"),
                        "last_name": platform_user_info.get("last_name")
                    }
                elif context.platform_name == "instagram":
                    context.user_info = {
                        "name": platform_user_info.get("username"),
                        "username": platform_user_info.get("username")
                    }
            except Exception as e:
                logger.warning(f"Failed to get user info: {str(e)}")
            
            # 获取或创建客户
            customer = conversation_manager.get_or_create_customer(
                platform=context.platform_name,
                platform_user_id=sender_id,
                name=context.user_info.get("name")
            )
            
            context.customer = customer
            context.customer_id = customer.id
            
            return ProcessorResult(
                status=ProcessorStatus.SUCCESS,
                message="客户信息处理成功",
                data={"customer_id": customer.id}
            )
        except Exception as e:
            logger.error(f"Error in user info handler: {str(e)}", exc_info=True)
            return ProcessorResult(
                status=ProcessorStatus.ERROR,
                message=f"用户信息处理失败: {str(e)}",
                error=e
            )


class FilterHandler(BaseProcessor):
    """过滤处理器 - 应用过滤规则"""
    
    def __init__(self):
        super().__init__("filter_handler", "消息过滤")
    
    def get_dependencies(self) -> list:
        return ["user_info_handler"]
    
    async def process(self, context: ProcessorContext) -> ProcessorResult:
        """应用过滤规则"""
        try:
            from src.collector.filter_engine import FilterEngine
            from src.database.models import Conversation
            
            filter_engine = FilterEngine(context.db)
            message_content = context.message_data.get("content", "")
            message_type = context.message_data.get("message_type", MessageType.MESSAGE)
            
            # 创建临时对话对象用于过滤
            temp_conversation = Conversation(
                customer_id=context.customer_id,
                platform_message_id=context.message_data.get("message_id"),
                message_type=message_type,
                content=message_content
            )
            
            filter_result = filter_engine.filter_message(temp_conversation, message_content)
            context.filter_result = filter_result
            context.should_review = filter_result.get("should_review", False)
            
            # 如果被过滤且不需要审核，跳过后续处理
            if filter_result.get("filtered") and not filter_result.get("should_review"):
                return ProcessorResult(
                    status=ProcessorStatus.SKIP,
                    message="消息已被过滤，跳过处理",
                    should_continue=False
                )
            
            return ProcessorResult(
                status=ProcessorStatus.SUCCESS,
                message="过滤处理完成",
                data={"filtered": filter_result.get("filtered", False)}
            )
        except Exception as e:
            logger.error(f"Error in filter handler: {str(e)}", exc_info=True)
            return ProcessorResult(
                status=ProcessorStatus.ERROR,
                message=f"过滤处理失败: {str(e)}",
                error=e
            )


class AIReplyHandler(BaseProcessor):
    """AI回复处理器"""
    
    def __init__(self):
        super().__init__("ai_reply_handler", "AI自动回复")
    
    def get_dependencies(self) -> list:
        return ["filter_handler"]
    
    async def process(self, context: ProcessorContext) -> ProcessorResult:
        """生成并发送AI回复"""
        try:
            from src.config.page_settings import page_settings
            from src.ai.reply_generator import ReplyGenerator
            from src.statistics.tracker import StatisticsTracker
            
            # 检查是否启用自动回复
            page_id = context.message_data.get("page_id")
            auto_reply_enabled = page_settings.is_auto_reply_enabled(page_id)
            
            if not auto_reply_enabled:
                logger.info(f"页面 {page_id or '未知'} 的自动回复已禁用")
                return ProcessorResult(
                    status=ProcessorStatus.SKIP,
                    message="自动回复已禁用",
                    should_continue=True  # 继续后续处理
                )
            
            # 生成AI回复
            reply_generator = ReplyGenerator(context.db)
            ai_reply = await reply_generator.generate_reply(
                customer_id=context.customer_id,
                message_content=context.message_data.get("content", ""),
                customer_name=context.customer.name if context.customer else None
            )
            
            if not ai_reply:
                return ProcessorResult(
                    status=ProcessorStatus.SKIP,
                    message="AI回复生成失败",
                    should_continue=True
                )
            
            context.ai_reply = ai_reply
            context.ai_replied = True
            
            # 检查是否包含群组邀请
            context.group_invitation_sent = "t.me" in ai_reply or "telegram" in ai_reply.lower()
            
            # 记录高频问题
            stats_tracker = StatisticsTracker(context.db)
            if context.message_summary:
                question_category = self._categorize_question(context.message_summary)
                stats_tracker.record_frequent_question(
                    question_text=context.message_summary,
                    category=question_category,
                    sample_response=ai_reply[:200]
                )
            
            # 发送回复到平台
            message_type = context.message_data.get("message_type", MessageType.MESSAGE)
            sender_id = context.message_data.get("sender_id")
            
            if message_type == MessageType.MESSAGE:
                await context.platform_client.send_message(
                    recipient_id=sender_id,
                    message=ai_reply
                )
            elif message_type == MessageType.COMMENT and context.platform_name == "facebook":
                from src.facebook.api_client import FacebookAPIClient
                if isinstance(context.platform_client, FacebookAPIClient):
                    post_id = context.message_data.get("post_id")
                    if post_id:
                        await context.platform_client.comment_on_post(post_id, ai_reply)
            
            return ProcessorResult(
                status=ProcessorStatus.SUCCESS,
                message="AI回复发送成功",
                data={"ai_reply": ai_reply[:100]}
            )
        except Exception as e:
            logger.error(f"Error in AI reply handler: {str(e)}", exc_info=True)
            return ProcessorResult(
                status=ProcessorStatus.ERROR,
                message=f"AI回复处理失败: {str(e)}",
                error=e
            )
    
    def _categorize_question(self, message: str) -> str:
        """问题分类"""
        message_lower = message.lower()
        if any(word in message_lower for word in ["price", "cost", "how much", "多少钱", "价格"]):
            return "价格咨询"
        elif any(word in message_lower for word in ["interest", "rate", "利息", "利率"]):
            return "利息咨询"
        elif any(word in message_lower for word in ["how", "how to", "怎么", "如何"]):
            return "流程咨询"
        elif any(word in message_lower for word in ["model", "型号", "iphone"]):
            return "产品咨询"
        return None


class DataCollectionHandler(BaseProcessor):
    """数据收集处理器"""
    
    def __init__(self):
        super().__init__("data_collection_handler", "数据收集")
    
    def get_dependencies(self) -> list:
        return ["message_receiver"]
    
    async def process(self, context: ProcessorContext) -> ProcessorResult:
        """收集数据（已在MessageReceiver中完成，这里只是确认）"""
        # 数据收集已在MessageReceiver中完成
        return ProcessorResult(
            status=ProcessorStatus.SUCCESS,
            message="数据收集完成",
            data={"extracted_info": context.extracted_info}
        )


class StatisticsHandler(BaseProcessor):
    """统计处理器 - 记录交互统计"""
    
    def __init__(self):
        super().__init__("statistics_handler", "统计记录")
    
    def get_dependencies(self) -> list:
        return ["user_info_handler", "ai_reply_handler"]
    
    async def process(self, context: ProcessorContext) -> ProcessorResult:
        """记录客户交互统计"""
        try:
            from src.statistics.tracker import StatisticsTracker
            
            stats_tracker = StatisticsTracker(context.db)
            
            message_type = context.message_data.get("message_type", MessageType.MESSAGE)
            message_type_str = message_type.value if hasattr(message_type, 'value') else str(message_type)
            
            interaction = stats_tracker.record_customer_interaction(
                customer_id=context.customer_id,
                platform=context.platform_name,
                message_type=message_type_str,
                message_summary=context.message_summary,
                extracted_info=context.extracted_info,
                ai_replied=context.ai_replied,
                group_invitation_sent=context.group_invitation_sent
            )
            
            return ProcessorResult(
                status=ProcessorStatus.SUCCESS,
                message="统计记录成功",
                data={"interaction_id": interaction.id}
            )
        except Exception as e:
            logger.error(f"Error in statistics handler: {str(e)}", exc_info=True)
            return ProcessorResult(
                status=ProcessorStatus.ERROR,
                message=f"统计记录失败: {str(e)}",
                error=e
            )


class NotificationHandler(BaseProcessor):
    """通知处理器 - 发送Telegram通知"""
    
    def __init__(self):
        super().__init__("notification_handler", "Telegram通知")
    
    def get_dependencies(self) -> list:
        return ["filter_handler"]
    
    async def process(self, context: ProcessorContext) -> ProcessorResult:
        """发送Telegram通知（如果需要审核）"""
        try:
            if not context.should_review:
                return ProcessorResult(
                    status=ProcessorStatus.SKIP,
                    message="不需要审核，跳过通知"
                )
            
            from src.telegram.notification_sender import NotificationSender
            from src.database.models import Conversation
            
            notification_sender = NotificationSender()
            
            # 创建临时对话对象用于通知
            temp_conversation = Conversation(
                customer_id=context.customer_id,
                platform_message_id=context.message_data.get("message_id"),
                message_type=context.message_data.get("message_type", MessageType.MESSAGE),
                content=context.message_summary
            )
            
            await notification_sender.send_review_notification(
                conversation=temp_conversation,
                customer=context.customer,
                collected_data=None
            )
            
            await notification_sender.close()
            
            return ProcessorResult(
                status=ProcessorStatus.SUCCESS,
                message="通知发送成功"
            )
        except Exception as e:
            logger.error(f"Error in notification handler: {str(e)}", exc_info=True)
            return ProcessorResult(
                status=ProcessorStatus.ERROR,
                message=f"通知发送失败: {str(e)}",
                error=e
            )


