# 路由逻辑

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from ..schemas import TaskCreate, TaskResponse, PaginatedTaskResponse, TaskUpdate
from ..database import SessionLocal, Task
from sqlalchemy.orm import Session
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
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    # 构建基础查询
    query = db.query(Task)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    tasks = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # 计算总页数
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "items": tasks,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": total_pages
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