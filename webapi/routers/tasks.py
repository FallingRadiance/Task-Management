# 路由逻辑

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from ..schemas import TaskCreate, TaskResponse, PaginatedTaskResponse, TaskUpdate
from ..database import SessionLocal, Task
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["tasks"])

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建新任务
@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info(f"创建新任务: ID={db_task.id}, 标题='{db_task.title}'")
    return db_task

# 获取任务列表（带过滤）
@router.get("/", response_model=PaginatedTaskResponse)
async def read_tasks(
    search: Optional[str] = Query(None, description="搜索标题和描述"),
    completed: Optional[bool] = Query(None, description="完成状态"),
    priority: Optional[str] = Query(None, description="优先级"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    query = db.query(Task)

    # 搜索功能
    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
        )

    # 完成状态过滤
    if completed is not None:
        query = query.filter(Task.completed == completed)

    # 优先级过滤
    if priority:
        query = query.filter(Task.priority == priority)

    # 日期范围过滤
    if start_date:
        start_datetime = datetime.strptime(f"{start_date} 00:00:00", "%Y-%m-%d %H:%M:%S")
        query = query.filter(Task.start_time >= start_datetime)
    if end_date:
        end_datetime = datetime.strptime(f"{end_date} 23:59:59", "%Y-%m-%d %H:%M:%S")
        query = query.filter(Task.end_time <= end_datetime)

    # 计算总数
    total = query.count()
    
    # 分页
    tasks = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "items": tasks,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size
    }

# 获取单个任务
@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# 更新任务
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

# 删除任务
@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        logger.warning(f"尝试删除不存在的任务: ID={task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    logger.info(f"删除任务: ID={task_id}")
    return None