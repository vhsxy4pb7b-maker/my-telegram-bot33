# 模块化架构文档

## 📋 概述

本项目已重构为模块化架构，便于后期升级和维护。所有工具和配置管理都采用统一的接口和插件系统。

## 🏗️ 架构设计

### 1. 工具模块 (`src/tools/`)

所有工具都继承自 `BaseTool` 基类，提供统一的接口：

```
src/tools/
├── __init__.py           # 模块导出
├── base.py               # 工具基类和接口
├── registry.py           # 工具注册器（单例模式）
├── cli.py                # 命令行接口
├── plugin_base.py        # 插件系统基类
├── token_manager.py       # 令牌管理工具
├── config_checker.py     # 配置检查工具
├── permission_checker.py  # 权限检查工具
└── exchange_token_tool.py # 令牌交换工具
```

#### 工具基类

所有工具都继承 `BaseTool`：

```python
from src.tools import BaseTool, ToolResult, ToolStatus

class MyTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="我的工具描述"
        )
    
    async def execute(self, **kwargs) -> ToolResult:
        # 实现工具逻辑
        return ToolResult(
            status=ToolStatus.SUCCESS,
            message="执行成功",
            data={'result': '...'}
        )
```

#### 工具注册

工具会自动注册到注册器：

```python
from src.tools import registry

# 注册工具
registry.register("my_tool", MyTool)

# 创建工具实例
tool = registry.create_tool("my_tool")

# 执行工具
result = await tool.execute(param1="value1")
```

### 2. 业务服务层 (`src/business/`)

业务服务层将业务逻辑与处理流程解耦，便于扩展和维护：

```
src/business/
├── __init__.py              # 模块导出和自动注册
├── registry.py              # 业务服务注册器
├── services/                # 业务服务实现
│   ├── base_service.py      # 业务服务基类
│   ├── auto_reply_service.py    # AI自动回复服务（已实现）
│   ├── post_service.py          # 发帖服务（预留接口）
│   ├── ad_service.py            # 广告管理服务（预留接口）
│   └── material_generation_service.py  # 素材生成服务（预留接口）
└── modules/                 # 可插拔业务模块
    ├── customer_service/    # 客服业务模块（已实现）
    │   ├── config.py        # 模块配置
    │   └── workflows.py     # 工作流定义
    └── marketing_module/    # 营销业务模块（预留框架）
        ├── config.py        # 模块配置
        ├── workflows.py     # 工作流定义
        ├── scheduler.py     # 定时任务调度器
        └── material_integration.py  # 素材生成集成点
```

#### 业务服务基类

所有业务服务继承 `BaseBusinessService`：

```python
from src.business.services.base_service import BaseBusinessService

class MyBusinessService(BaseBusinessService):
    def __init__(self):
        super().__init__("my_service", "我的业务服务")
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # 实现业务逻辑
        return {"success": True, "message": "处理成功"}
```

#### 业务服务注册

业务服务通过注册器管理：

```python
from src.business.registry import business_registry
from src.business.services.my_service import MyBusinessService

# 注册服务
business_registry.register("my_service", MyBusinessService)

# 获取服务实例
service = business_registry.get("my_service")
result = await service.execute(context)
```

### 3. 配置模块 (`src/config/`)

配置管理已模块化：

```
src/config/
├── __init__.py      # 模块导出
├── settings.py      # 应用设置（从环境变量加载）
├── loader.py        # 配置文件加载器
└── validators.py    # 配置验证器
```

#### 使用配置

```python
from src.config import settings, ConfigValidator

# 访问配置
token = settings.facebook_access_token

# 验证配置
validator = ConfigValidator(settings)
result = validator.validate_facebook_config()
```

### 4. 插件系统

支持动态加载插件：

```python
from src.tools import Plugin, PluginManager, plugin_manager

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__("my_plugin", "1.0.0")
    
    def get_tools(self):
        return [MyTool()]
    
    def get_dependencies(self):
        return []  # 依赖的插件列表

# 注册插件
plugin_manager.set_tool_registry(registry)
plugin_manager.register_plugin(MyPlugin())
```

## 🚀 使用示例

### 命令行使用

```bash
# 列出所有工具
python -m src.tools.cli list

# 使用工具
python -m src.tools.cli token_manager --action extract --url "..."

# 查看帮助
python -m src.tools.cli help token_manager
```

### 编程使用

```python
from src.tools import TokenManager, registry
import asyncio

async def main():
    # 方式1：直接使用工具类
    manager = TokenManager()
    result = await manager.execute(action='extract', url='...')
    
    # 方式2：通过注册器
    tool = registry.create_tool('token_manager')
    result = await tool.execute(action='extract', url='...')
    
    if result.is_success():
        print(f"成功: {result.message}")
        print(f"数据: {result.data}")
    else:
        print(f"失败: {result.message}")
        for error in result.errors:
            print(f"  - {error}")

asyncio.run(main())
```

## 📦 添加新工具

### 步骤1：创建工具类

```python
# src/tools/my_new_tool.py
from src.tools import BaseTool, ToolResult, ToolStatus

class MyNewTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_new_tool",
            description="我的新工具"
        )
    
    async def execute(self, **kwargs) -> ToolResult:
        # 实现工具逻辑
        return ToolResult(
            status=ToolStatus.SUCCESS,
            message="执行成功"
        )
```

### 步骤2：注册工具

```python
# src/tools/__init__.py
from .my_new_tool import MyNewTool

# 在 registry.py 中注册
registry.register("my_new_tool", MyNewTool)
```

### 步骤3：使用工具

```bash
python -m src.tools.cli my_new_tool --param1 value1
```

## 🔌 插件开发

### 创建插件

```python
from src.tools import Plugin, BaseTool

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__("my_plugin", "1.0.0")
    
    def get_tools(self):
        return [
            MyTool1(),
            MyTool2(),
        ]
    
    def get_dependencies(self):
        return []  # 依赖列表
    
    def on_load(self):
        print("插件已加载")
    
    def on_unload(self):
        print("插件已卸载")
```

### 加载插件

```python
from src.tools import plugin_manager, registry

plugin_manager.set_tool_registry(registry)
plugin_manager.register_plugin(MyPlugin())

# 列出所有插件
for plugin_info in plugin_manager.list_plugins():
    print(plugin_info)
```

## 🎯 优势

### 1. 模块化
- 每个工具独立实现
- 清晰的接口定义
- 易于测试和维护

### 2. 可扩展性
- 插件系统支持动态扩展
- 新工具只需实现接口即可
- 无需修改核心代码

### 3. 统一接口
- 所有工具使用相同的接口
- 统一的错误处理
- 一致的返回格式

### 4. 易于升级
- 向后兼容
- 平滑迁移
- 版本管理

## 📝 迁移指南

### 从旧脚本迁移

Token提取功能已集成到工具系统中，建议使用新的工具系统：

```python
# 使用工具系统
from src.tools import TokenManager
manager = TokenManager()
result = await manager.execute(action='extract', url=url)
if result.is_success():
    token_info = result.data
```

## 🔄 版本兼容

- 保持 `src/config.py` 向后兼容
- 旧脚本可以继续使用
- 新功能使用模块化系统

## 📚 相关文档

- [工具开发指南](docs/tool_development.md)
- [插件开发指南](docs/plugin_development.md)
- [配置管理指南](docs/configuration.md)
- [业务模块扩展指南](../guides/BUSINESS_MODULE_EXTENSION.md)









