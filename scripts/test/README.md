# 测试脚本使用说明

## 快速测试

### Windows
```bash
scripts\test\quick_test.bat
```

### Linux/Mac
```bash
chmod +x scripts/test/quick_test.sh
./scripts/test/quick_test.sh
```

快速测试脚本会检查：
- Python环境
- 依赖安装
- 配置文件
- 数据库连接
- 核心模块导入
- 应用启动

## 完整测试

### 运行所有测试
```bash
# Linux/Mac
chmod +x scripts/test/full_test.sh
./scripts/test/full_test.sh

# 或使用pytest
pytest tests/ -v --cov=src --cov-report=term
```

### 运行特定测试
```bash
# 系统功能测试
python tests/test_system_functionality.py

# 生产就绪性测试
python tests/test_production_readiness.py

# API端点测试
pytest tests/test_api_endpoints.py -v

# 集成测试
pytest tests/test_integration.py -v

# 端到端测试
pytest tests/test_e2e_workflow.py -v
```

## 生成测试报告

```bash
python scripts/test/generate_report.py
```

报告将保存在 `data/test_reports/` 目录下：
- JSON格式报告
- HTML格式报告（可在浏览器中查看）

## 部署验证

在部署到生产环境前，运行部署验证脚本：

### Windows
```bash
scripts\test\validate_deployment.bat
```

### Linux/Mac
```bash
chmod +x scripts/test/validate_deployment.sh
./scripts/test/validate_deployment.sh
```

验证脚本会检查：
- 配置文件完整性
- 环境变量配置
- 数据库连接
- 数据库迁移
- 应用启动
- API端点
- 日志目录

## 测试阶段

### 阶段一：基础环境测试
```bash
python -m pytest tests/test_system_functionality.py::test_config_loading -v
python -m pytest tests/test_system_functionality.py::test_database_connection -v
python tests/test_production_readiness.py
```

### 阶段二：核心功能测试
```bash
pytest tests/test_ai_reply_generator.py -v
pytest tests/test_data_collector.py -v
pytest tests/test_filter_engine.py -v
pytest tests/test_database_models.py -v
```

### 阶段三：API端点测试
```bash
# 启动服务
python run.py

# 在另一个终端测试
curl http://localhost:8000/health
curl http://localhost:8000/metrics
curl http://localhost:8000/admin/conversations?page=1&page_size=10
```

### 阶段四：集成测试
```bash
python tests/test_system_functionality.py
pytest tests/test_integration.py -v
```

### 阶段五：端到端测试
```bash
pytest tests/test_e2e_workflow.py -v
```

## 测试检查清单

### 必须通过的测试（阻塞性问题）
- [ ] 配置加载成功
- [ ] 数据库连接正常
- [ ] 应用可以启动
- [ ] 所有API端点可访问
- [ ] Facebook Webhook可以验证
- [ ] AI回复可以生成
- [ ] 数据可以收集和保存
- [ ] Telegram通知可以发送

### 建议通过的测试（非阻塞性）
- [ ] Instagram集成工作正常
- [ ] 统计功能正常
- [ ] 监控功能正常
- [ ] 管理后台API正常
- [ ] 性能指标正常

## 问题排查

如果测试失败：

1. **查看日志文件**: `logs/app.log`
2. **检查配置文件**: `.env` 和 `config/config.yaml`
3. **验证环境变量**: 确保所有必需的环境变量已设置
4. **检查数据库**: 确保数据库连接正常
5. **运行快速测试**: 使用 `quick_test.sh/bat` 快速定位问题

## 持续集成

测试脚本可以在CI/CD流程中使用：

```yaml
# .github/workflows/ci.yml 示例
- name: Run tests
  run: |
    pytest tests/ -v --cov=src --cov-report=xml
    
- name: Generate test report
  run: |
    python scripts/test/generate_report.py
```

