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
启动后端服务之后，在浏览器中打开 `frontend/index.html`，即可启动前端页面，进行任务的增删查改

---
## 使用说明
（*注意*：前端页面是应检测功能所写，暂无美观的界面）

### 添加任务
用户在“创建新任务”下输入
- 标题（必选）
- 描述（可选）
- 开始时间/结束时间（可选）
  
点击“创建任务”按钮，即可新建一个任务

### 查询任务
查询分为“过滤”与“高级查询”

- 过滤
  用户可在过滤任务的下拉菜单中选择：
  - 所有任务
  - 已完成
  - 未完成
  对应的任务将显示在界面中

- 高级查询
  用户可选择以下限制：
  - 标题含有的字符
  - 任务的起止日期（此功能可能存在bug）
  （优先级功能暂缺）
  选择（填入）对应的限制后，页面将只显示符合要求的任务

---
## 检查和测试

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