"""主消息处理流程 - 使用模块化管道"""
from src.processors.pipeline import default_pipeline
import logging

logger = logging.getLogger(__name__)


async def process_platform_message(platform_name: str, message_data: dict):
    """
    统一处理平台消息的完整流程（使用模块化管道）
    
    流程通过管道模式执行，每个步骤都是独立的处理器：
    1. 消息接收 → 2. 用户信息处理 → 3. 过滤处理 → 4. AI回复 → 5. 数据收集 → 6. 统计记录 → 7. 通知发送
    
    Args:
        platform_name: 平台名称（如 'facebook', 'instagram'）
        message_data: 消息数据字典
    """
    try:
        # 使用默认管道处理消息
        result = await default_pipeline.process(platform_name, message_data)
        
        if result.get("success"):
            logger.info(f"Successfully processed {platform_name} message for customer {result.get('customer_id')}")
        else:
            logger.error(f"Failed to process {platform_name} message: {result.get('error')}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error processing {platform_name} message: {str(e)}", exc_info=True)
        return {"success": False, "error": str(e)}


async def process_facebook_message(message_data: dict):
    """
    处理 Facebook 消息的完整流程（兼容层）
    
    流程：
    1. 接收消息 → 2. AI 自动回复 → 3. 资料收集与过滤 → 4. Telegram 通知 → 5. 人工审核
    """
    # 添加平台标识并调用统一处理器
    message_data["platform"] = "facebook"
    await process_platform_message("facebook", message_data)
