from fastapi import FastAPI
from contextlib import asynccontextmanager
from webapi.routers import tasks
from .database import engine, Base
import logging
import os
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware
from .exceptions import create_exception_handlers

# 确保logs目录存在
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志
logging.basicConfig(
    filename=os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 确保数据库表已创建
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

# 注册异常处理器
create_exception_handlers(app)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=False,  # 使用通配符时必须为 False
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
    expose_headers=["*"],  # 暴露所有响应头

    # allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    # allow_credentials=True,
    # allow_methods=["*"],
    # allow_headers=["*"],

)

# 包含路由
app.include_router(tasks.router)

# 添加根路由
@app.get("/")
async def root():
    return {"message": "任务管理系统 API 运行正常"}