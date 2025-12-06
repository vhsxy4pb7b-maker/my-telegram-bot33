"""AI 回复模板和提示词管理"""
from typing import Dict, Any, Optional
from src.config import yaml_config


class PromptTemplates:
    """提示词模板管理"""
    
    def __init__(self):
        self.templates = yaml_config.get("ai_templates", {})
    
    def get_greeting(self) -> str:
        """获取问候语模板"""
        return self.templates.get(
            "greeting",
            "您好！感谢您的咨询，我是AI智能客服，很高兴为您服务。"
        )
    
    def get_collecting_info(self) -> str:
        """获取收集信息提示"""
        return self.templates.get(
            "collecting_info",
            "为了更好地帮助您，请提供以下信息：姓名、联系方式、具体需求。"
        )
    
    def get_processing(self) -> str:
        """获取处理中提示"""
        return self.templates.get(
            "processing",
            "正在为您处理，请稍候..."
        )
    
    def get_fallback(self) -> str:
        """获取默认回复"""
        return self.templates.get(
            "fallback",
            "抱歉，我没有完全理解您的问题。能否详细描述一下您的需求？"
        )
    
    def build_system_prompt(self, prompt_type: Optional[str] = None) -> str:
        """
        构建系统提示词
        
        Args:
            prompt_type: 提示词类型，如果为 'iphone_loan_telegram' 则使用专用提示词
            
        Returns:
            系统提示词字符串
        """
        # 检查是否使用专用提示词
        if prompt_type == "iphone_loan_telegram":
            try:
                from src.ai.prompts.iphone_loan_telegram import IPHONE_LOAN_TELEGRAM_PROMPT
                prompt = IPHONE_LOAN_TELEGRAM_PROMPT
                
                # 从配置中读取Telegram群组/频道名称并替换
                telegram_config = yaml_config.get("telegram_groups", {})
                main_group = telegram_config.get("main_group", "@your_group")
                main_channel = telegram_config.get("main_channel", "@your_channel")
                
                # 替换提示词中的占位符
                prompt = prompt.replace("@your_group", main_group)
                prompt = prompt.replace("@your_channel", main_channel)
                
                return prompt
            except ImportError:
                # 如果导入失败，使用默认提示词
                pass
        
        # 检查配置文件中是否有自定义提示词
        custom_prompt = self.templates.get("system_prompt")
        if custom_prompt:
            return custom_prompt
        
        # 默认提示词
        return """You are a professional AI customer service assistant. Your responsibilities are:
1. Reply to customer inquiries in a friendly and professional manner
2. Collect basic customer information (name, contact, needs, etc.)
3. Understand customer intent and provide initial assistance
4. If unable to resolve, guide customers to provide more information for manual processing

Please reply in the same language as the customer, maintaining politeness and professionalism."""
    
    def build_conversation_context(
        self,
        customer_name: str = None,
        previous_messages: list = None
    ) -> str:
        """构建对话上下文"""
        context = ""
        
        if customer_name:
            context += f"客户姓名：{customer_name}\n"
        
        if previous_messages:
            context += "\n历史对话：\n"
            for msg in previous_messages[-5:]:  # 只保留最近5条
                role = "客户" if msg.get("role") == "user" else "客服"
                content = msg.get("content", "")
                context += f"{role}：{content}\n"
        
        return context


