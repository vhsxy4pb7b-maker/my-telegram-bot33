# 统计数据快速参考

## 🚀 快速查看统计

### 命令行工具
```bash
python view_statistics.py
```

### API接口
```bash
# 今日统计
curl http://localhost:8000/statistics/daily

# 高频问题
curl http://localhost:8000/statistics/frequent-questions
```

## 📊 关键指标

- **总接待客户数** - 每天接待了多少客户
- **成功引流数** - 加入群组的客户数
- **开单数** - 成功开单的客户数
- **引流转化率** - 邀请到加入的转化率
- **开单转化率** - 引流到开单的转化率

## ✅ 重要说明

1. **不保存详细聊天记录** - 只保存消息摘要（500字符）
2. **统计数据自动更新** - 每次交互自动计算
3. **手动标记** - 加入群组和开单需要手动标记

## 🔧 手动标记

### 标记加入群组
```bash
curl -X POST "http://localhost:8000/statistics/mark-joined-group?customer_id=123"
```

### 标记开单
```bash
curl -X POST "http://localhost:8000/statistics/mark-order-created?customer_id=123"
```

详细文档：`STATISTICS_GUIDE.md`


