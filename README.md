# 任务管理系统

## 启动说明

### 后端服务
```bash
# 在task目录下执行
uvicorn webapi.main:app --reload --host 0.0.0.0
```
服务将在以下地址运行：
- API服务：http://127.0.0.1:8000
- API文档：http://127.0.0.1:8000/docs
- 任务接口：http://127.0.0.1:8000/tasks/

### 前端页面
启动后端服务之后，在浏览器中打开 `frontend/index.html`，即可进行任务的增删查改

### 服务检查
在`task`目录下执行
```bash
python check_service.py
```

### 运行测试
```bash
# 安装测试依赖
pip install pytest pytest-cov pytest-asyncio httpx

# 运行基本测试
pytest webapi/tests/ -v

# 查看详细输出
pytest webapi/tests/ -v -s

# 生成测试覆盖率报告
pytest --cov=webapi webapi/tests/ -v

# 生成HTML格式的覆盖率报告
pytest --cov=webapi --cov-report=html webapi/tests/ -v
```

测试覆盖率报告将生成在 `htmlcov` 目录中，可以在浏览器中打开 `htmlcov/index.html` 查看详细报告。