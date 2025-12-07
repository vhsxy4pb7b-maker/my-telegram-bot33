# 实时监控系统使用指南

## 📋 概述

实时监控系统允许你实时查看AI的工作情况，包括：
- ✅ 实时AI回复内容和数量
- ✅ 客户信息和平台分布
- ✅ 今日统计和最近1小时数据
- ✅ 系统事件和错误

## 🚀 快速开始

### 方法1：使用监控面板（推荐）

1. **打开监控面板**
   - 在浏览器中打开 `monitoring_dashboard.html`
   - 或者访问：`https://你的域名/monitoring/dashboard`（如果部署了静态文件）

2. **查看实时数据**
   - 面板会自动连接并显示实时AI回复
   - 统计数据每5秒自动更新
   - 新的AI回复会实时显示在顶部

### 方法2：使用API接口

#### 实时流（Server-Sent Events）

```bash
# 连接实时事件流
curl -N https://你的域名/monitoring/live
```

**返回格式**：
```
data: {"type":"ai_reply","timestamp":"2024-12-07T12:00:00","data":{...}}

data: {"type":"system_event","event_type":"info","message":"..."}
```

#### 获取实时统计

```bash
# 获取当前统计数据
curl https://你的域名/monitoring/stats
```

**返回示例**：
```json
{
  "success": true,
  "data": {
    "today": {
      "total_replies": 45,
      "unique_customers": 32
    },
    "last_hour": {
      "replies": 8
    },
    "platform_distribution": {
      "facebook": 30,
      "instagram": 15
    }
  }
}
```

#### 获取最近的回复记录

```bash
# 获取最近20条AI回复
curl https://你的域名/monitoring/recent-replies?limit=20
```

## 📊 API端点说明

### 1. `/monitoring/live` - 实时事件流

**类型**: Server-Sent Events (SSE)

**功能**: 实时推送AI回复和系统事件

**事件类型**:
- `ai_reply`: AI回复事件
- `system_event`: 系统事件（错误、警告等）
- `connected`: 连接成功
- `initial_data`: 初始数据

**使用示例**:
```javascript
const eventSource = new EventSource('/monitoring/live');

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('收到事件:', data);
};
```

### 2. `/monitoring/stats` - 实时统计

**方法**: GET

**功能**: 获取当前的实时统计数据

**返回数据**:
- `today.total_replies`: 今日总回复数
- `today.unique_customers`: 今日唯一客户数
- `last_hour.replies`: 最近1小时回复数
- `platform_distribution`: 平台分布统计

### 3. `/monitoring/recent-replies` - 最近回复

**方法**: GET

**参数**:
- `limit` (可选): 返回数量，默认20

**功能**: 获取最近的AI回复记录

## 🎨 监控面板功能

### 实时显示

- **连接状态**: 显示当前连接状态（已连接/断开）
- **统计数据**: 实时显示今日回复数、客户数、最近1小时数据
- **回复记录**: 实时显示每条AI回复，包括：
  - 客户信息
  - 平台标识（Facebook/Instagram）
  - 用户消息
  - AI回复内容
  - 时间戳

### 自动更新

- 统计数据每5秒自动刷新
- 新的AI回复实时显示（无需刷新页面）
- 自动重连机制（连接断开后5秒自动重连）

## 🔧 集成到现有系统

### 在AI回复处理器中自动记录

系统已自动集成，每次AI回复时会自动记录到实时监控系统。

### 手动记录系统事件

```python
from src.monitoring.realtime import realtime_monitor

# 记录系统事件
await realtime_monitor.record_system_event(
    event_type="info",
    message="系统启动",
    data={"version": "2.0.0"}
)
```

## 📱 移动端支持

监控面板响应式设计，支持移动设备访问。

## 🔒 安全建议

1. **生产环境**: 建议添加身份验证
2. **HTTPS**: 使用HTTPS确保数据传输安全
3. **访问控制**: 限制监控面板的访问权限

## 🐛 故障排除

### 连接断开

- 检查网络连接
- 检查服务器是否运行
- 查看浏览器控制台错误信息

### 没有数据显示

- 确认AI回复功能正常工作
- 检查数据库连接
- 查看服务器日志

### 统计数据不更新

- 刷新页面
- 检查API端点是否可访问
- 查看浏览器网络请求

## 📈 性能优化

- 监控系统使用内存缓存，不影响主系统性能
- 保留最近100条回复记录（可配置）
- SSE连接自动清理断开的连接

## 🎯 下一步

- [ ] 添加身份验证
- [ ] 添加数据导出功能
- [ ] 添加图表可视化
- [ ] 添加告警功能
- [ ] 添加历史数据查询

