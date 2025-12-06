"""命令行接口 - 提供统一的CLI入口"""
import sys
import asyncio
from typing import Dict, Any, Optional
from .registry import registry
from .base import BaseTool, ToolResult


class CLI:
    """命令行接口管理器"""
    
    def __init__(self):
        self.registry = registry
    
    def print_result(self, result: ToolResult):
        """打印工具执行结果"""
        from .base import ToolStatus
        
        status_icons = {
            ToolStatus.SUCCESS: "✅",
            ToolStatus.WARNING: "⚠️",
            ToolStatus.ERROR: "❌",
            ToolStatus.INFO: "ℹ️"
        }
        
        icon = status_icons.get(result.status, "•")
        print(f"\n{icon} {result.message}")
        
        if result.data:
            print("\n数据:")
            for key, value in result.data.items():
                print(f"  {key}: {value}")
        
        if result.errors:
            print("\n错误/警告:")
            for error in result.errors:
                print(f"  - {error}")
    
    async def run_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """
        运行工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            工具执行结果
        """
        from .base import ToolStatus
        
        tool = self.registry.create_tool(tool_name)
        if not tool:
            return ToolResult(
                status=ToolStatus.ERROR,
                message=f"工具 '{tool_name}' 未找到",
                errors=[f"可用工具: {', '.join(self.registry.list_tools())}"]
            )
        
        from .base import ToolStatus
        
        # 验证输入
        validation_error = tool.validate_input(**kwargs)
        if validation_error:
            return ToolResult(
                status=ToolStatus.ERROR,
                message="输入验证失败",
                errors=[validation_error]
            )
        
        # 执行工具
        return await tool.execute(**kwargs)
    
    def show_help(self, tool_name: Optional[str] = None):
        """显示帮助信息"""
        if tool_name:
            tool = self.registry.create_tool(tool_name)
            if tool:
                print(tool.get_help())
            else:
                print(f"工具 '{tool_name}' 未找到")
        else:
            print("可用工具:")
            for name in self.registry.list_tools():
                tool = self.registry.create_tool(name)
                if tool:
                    print(f"  {name}: {tool.description}")


async def main():
    """主函数 - CLI入口"""
    cli = CLI()
    
    if len(sys.argv) < 2:
        cli.show_help()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "help" or command == "--help" or command == "-h":
        tool_name = sys.argv[2] if len(sys.argv) > 2 else None
        cli.show_help(tool_name)
        return
    
    if command == "list":
        print("已注册的工具:")
        for name in cli.registry.list_tools():
            print(f"  - {name}")
        return
    
    # 解析参数
    tool_name = command
    kwargs = {}
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg.startswith("--"):
            key = arg[2:]
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
                value = sys.argv[i + 1]
                kwargs[key] = value
                i += 2
            else:
                kwargs[key] = True
                i += 1
        else:
            i += 1
    
    # 运行工具
    result = await cli.run_tool(tool_name, **kwargs)
    cli.print_result(result)
    
    # 根据结果设置退出码
    sys.exit(0 if result.is_success() else 1)


if __name__ == "__main__":
    asyncio.run(main())

