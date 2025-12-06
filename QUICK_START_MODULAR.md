# 模块化系统快速开始

## 🚀 快速使用

### 1. 使用工具

```python
from src.tools import TokenManager, ConfigChecker, PermissionChecker
import asyncio

async def main():
    # 令牌管理
    manager = TokenManager()
    result = await manager.execute(
        action='extract',
        url='http://localhost:8000/oauth/callback#access_token=...'
    )
    
    # 配置检查
    checker = ConfigChecker()
    result = await checker.execute(type='facebook')
    
    # 权限检查
    perm_checker = PermissionChecker()
    result = await perm_checker.execute(
        access_token='your_token_here'
    )

asyncio.run(main())
```

### 2. 命令行使用

```bash
# 列出所有工具
python -m src.tools.cli list

# 提取令牌
python -m src.tools.cli token_manager --action extract --url "..."

# 检查配置
python -m src.tools.cli config_checker --type facebook

# 检查权限
python -m src.tools.cli permission_checker --access_token "..."

# 交换令牌
python -m src.tools.cli exchange_token --short_token "..." --app_id "..." --app_secret "..."
```

### 3. 通过注册器使用

```python
from src.tools import registry

# 创建工具实例
tool = registry.create_tool('token_manager')

# 执行工具
result = await tool.execute(action='extract', url='...')

# 列出所有工具
for name in registry.list_tools():
    print(name)
```

## 📦 添加新工具

### 步骤1：创建工具类

```python
# src/tools/my_tool.py
from src.tools import BaseTool, ToolResult, ToolStatus

class MyTool(BaseTool):
    def __init__(self):
        super().__init__("my_tool", "我的工具")
    
    async def execute(self, **kwargs) -> ToolResult:
        param = kwargs.get('param')
        if not param:
            return ToolResult(
                status=ToolStatus.ERROR,
                message="缺少参数",
                errors=["param是必需的"]
            )
        
        return ToolResult(
            status=ToolStatus.SUCCESS,
            message="执行成功",
            data={'result': f"处理了 {param}"}
        )
```

### 步骤2：注册工具

在 `src/tools/registry.py` 中添加：

```python
from .my_tool import MyTool
registry.register("my_tool", MyTool)
```

### 步骤3：使用工具

```bash
python -m src.tools.cli my_tool --param value
```

## 🔌 创建插件

```python
from src.tools import Plugin, BaseTool

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__("my_plugin", "1.0.0")
    
    def get_tools(self):
        return [MyTool()]
    
    def get_dependencies(self):
        return []

# 注册插件
from src.tools import plugin_manager, registry
plugin_manager.set_tool_registry(registry)
plugin_manager.register_plugin(MyPlugin())
```

## 📋 工具结果

所有工具返回 `ToolResult`：

```python
result = await tool.execute(...)

# 检查状态
if result.is_success():
    print("成功")
    print(result.data)
elif result.has_warnings():
    print("有警告")
    for error in result.errors:
        print(f"  - {error}")
elif result.has_errors():
    print("有错误")
    for error in result.errors:
        print(f"  - {error}")
```

## 🎯 可用工具

| 工具名称 | 描述 | 使用示例 |
|---------|------|---------|
| `token_manager` | 令牌管理 | `--action extract --url "..."` |
| `config_checker` | 配置检查 | `--type facebook` |
| `permission_checker` | 权限检查 | `--access_token "..."` |
| `exchange_token` | 令牌交换 | `--short_token "..." --app_id "..." --app_secret "..."` |

## 📚 更多信息

- [完整架构文档](MODULAR_ARCHITECTURE.md)
- [工具模块文档](src/tools/README.md)
- [使用示例](examples/use_tools.py)



