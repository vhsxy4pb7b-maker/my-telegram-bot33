"""定时任务模块"""
import asyncio
from typing import List, Callable
import logging

logger = logging.getLogger(__name__)


class Scheduler:
    """简单的定时任务调度器"""
    
    def __init__(self):
        self.tasks: List[asyncio.Task] = []
    
    def add_periodic_task(
        self,
        func: Callable,
        interval_seconds: int,
        *args,
        **kwargs
    ):
        """
        添加周期性任务
        
        Args:
            func: 要执行的函数
            interval_seconds: 执行间隔（秒）
            *args, **kwargs: 传递给函数的参数
        """
        async def periodic():
            while True:
                try:
                    if asyncio.iscoroutinefunction(func):
                        await func(*args, **kwargs)
                    else:
                        func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in periodic task {func.__name__}: {str(e)}", exc_info=True)
                
                await asyncio.sleep(interval_seconds)
        
        task = asyncio.create_task(periodic())
        self.tasks.append(task)
        logger.info(f"Added periodic task: {func.__name__} (interval: {interval_seconds}s)")
    
    def cancel_all(self):
        """取消所有任务"""
        for task in self.tasks:
            task.cancel()
        self.tasks.clear()


# 全局调度器实例
scheduler = Scheduler()


# 示例：可以在这里添加定时任务
# async def cleanup_old_data():
#     """清理旧数据"""
#     # 实现清理逻辑
#     pass
#
# scheduler.add_periodic_task(cleanup_old_data, 3600)  # 每小时执行一次


