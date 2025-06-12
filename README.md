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
在浏览器中打开 `frontend/index.html`

### 服务检查
```bash
python check_service.py
```