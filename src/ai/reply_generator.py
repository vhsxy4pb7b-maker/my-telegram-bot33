"""AI 回复生成器"""
import openai
from typing import List, Dict, Any, Optional
from src.config import settings
from src.ai.prompt_templates import PromptTemplates
from src.ai.conversation_manager import ConversationManager
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


class ReplyGenerator:
    """使用 OpenAI API 生成智能回复"""
    
    def __init__(self, db: Session):
        self.db = db
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.templates = PromptTemplates()
        self.conversation_manager = ConversationManager(db)
    
    async def generate_reply(
        self,
        customer_id: int,
        message_content: str,
        customer_name: Optional[str] = None
    ) -> str:
        """
        生成 AI 回复
        
        Args:
            customer_id: 客户 ID
            message_content: 客户消息内容
            customer_name: 客户姓名
        
        Returns:
            AI 生成的回复内容
        """
        try:
            # 获取对话历史
            history = self.conversation_manager.get_conversation_history(
                customer_id,
                limit=10
            )
            
            # 获取提示词类型（从配置中读取）
            prompt_type = self.templates.templates.get("prompt_type")
            
            # 构建消息列表
            messages = [
                {
                    "role": "system",
                    "content": self.templates.build_system_prompt(prompt_type=prompt_type)
                }
            ]
            
            # 添加历史对话
            for msg in history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # 添加当前消息
            messages.append({
                "role": "user",
                "content": message_content
            })
            
            # 调用 OpenAI API
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                temperature=settings.openai_temperature,
                max_tokens=500
            )
            
            reply = response.choices[0].message.content.strip()
            
            logger.info(f"Generated reply for customer {customer_id}: {reply[:100]}...")
            
            return reply
        
        except Exception as e:
            logger.error(f"Error generating reply: {str(e)}", exc_info=True)
            # 返回默认回复
            return self.templates.get_fallback()
    
    def generate_greeting(self) -> str:
        """生成问候语"""
        return self.templates.get_greeting()
    
    def generate_collecting_info_prompt(self) -> str:
        """生成收集信息提示"""
        return self.templates.get_collecting_info()
    
    def should_collect_info(self, message_content: str) -> bool:
        """
        判断是否需要收集更多信息
        
        Args:
            message_content: 消息内容
        
        Returns:
            是否需要收集信息
        """
        # 简单的启发式规则
        # 可以后续用 AI 来判断
        info_keywords = ["姓名", "电话", "邮箱", "联系方式", "需求", "预算"]
        message_lower = message_content.lower()
        
        # 如果消息很短，可能需要更多信息
        if len(message_content) < 20:
            return True
        
        # 如果包含信息关键词，可能已经提供了信息
        if any(keyword in message_content for keyword in info_keywords):
            return False
        
        return True


