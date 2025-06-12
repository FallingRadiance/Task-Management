from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# 增
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

# 改
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

# 查
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

# 分页响应模型
class PaginatedTaskResponse(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int
    pages: int