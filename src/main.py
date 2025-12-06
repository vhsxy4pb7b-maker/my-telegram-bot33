"""FastAPI 主应用入口"""
from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.database.database import get_db, engine, Base
from src.facebook.webhook_handler import router as facebook_router
from src.instagram.webhook_handler import router as instagram_router
from src.telegram.bot_handler import router as telegram_router
from src.config import settings
import logging
import asyncio
from typing import Dict, Any, List

# 导入平台注册模块（确保平台被注册）
import src.facebook.register  # noqa: F401
import src.instagram.register  # noqa: F401

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="多平台客服自动化系统",
    description="支持 Facebook、Instagram 等多平台的自动化客服流程",
    version="2.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(facebook_router)  # Facebook Webhook (兼容路由: /webhook)
app.include_router(instagram_router)  # Instagram Webhook (/instagram/webhook)
app.include_router(telegram_router)

# 注册统计API路由
from src.statistics.api import router as statistics_router
app.include_router(statistics_router)


@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("Starting Multi-Platform Customer Service Automation System...")
    
    # 初始化平台管理器
    from src.platforms.manager import platform_manager
    
    # 初始化Facebook平台
    platform_manager.initialize_platform(
        platform_name="facebook",
        access_token=settings.facebook_access_token,
        verify_token=settings.facebook_verify_token
    )
    platform_manager.enable_platform("facebook")
    
    # 初始化Instagram平台（如果配置了）
    instagram_token = getattr(settings, 'instagram_access_token', None) or settings.facebook_access_token
    instagram_verify = getattr(settings, 'instagram_verify_token', None) or settings.facebook_verify_token
    instagram_user_id = getattr(settings, 'instagram_user_id', None)
    
    if instagram_token:
        try:
            # Instagram需要base_url参数
            platform_manager.initialize_platform(
                platform_name="instagram",
                access_token=instagram_token,
                verify_token=instagram_verify,
                base_url="https://graph.facebook.com/v18.0"
            )
            platform_manager.enable_platform("instagram")
            if instagram_user_id:
                logger.info(f"Instagram platform initialized (User ID: {instagram_user_id})")
            else:
                logger.warning("Instagram platform initialized but INSTAGRAM_USER_ID not configured - sending messages will fail")
        except Exception as e:
            logger.error(f"Failed to initialize Instagram platform: {str(e)}", exc_info=True)
    
    # 创建数据库表（如果不存在）
    # 注意：在生产环境建议使用 Alembic 迁移
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.warning(f"Database table creation skipped (may already exist): {str(e)}")
    
    # 列出已注册的平台
    from src.platforms.registry import registry
    logger.info(f"Registered platforms: {registry.list_platforms()}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info("Shutting down...")


@app.get("/")
async def root() -> Dict[str, Any]:
    """根路径"""
    from src.platforms.registry import registry
    return {
        "message": "多平台客服自动化系统",
        "version": "2.0.0",
        "status": "running",
        "supported_platforms": registry.list_platforms()
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """健康检查"""
    return {"status": "healthy"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

