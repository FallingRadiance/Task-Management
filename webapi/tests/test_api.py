import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db  # 使用相对导入
from ..main import app  # 使用相对导入

# 创建测试数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 覆盖依赖项
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

def test_create_task(test_db, client):
    response = client.post(
        "/tasks/",
        json={
            "title": "测试任务",
            "description": "测试描述",
            "start_time": "2025-06-12T10:00:00",
            "end_time": "2025-06-12T12:00:00"
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "测试任务"

def test_get_tasks(test_db, client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert "items" in response.json()

def test_delete_task(test_db, client):
    # 先创建一个任务
    create_response = client.post(
        "/tasks/",
        json={
            "title": "要删除的任务",
            "description": "这个任务将被删除"
        }
    )
    task_id = create_response.json()["id"]
    
    # 删除任务
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204
    
    # 确认任务已被删除
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_update_task(test_db, client):
    # 先创建一个任务
    create_response = client.post(
        "/tasks/",
        json={
            "title": "原始任务",
            "description": "这个任务将被更新"
        }
    )
    task_id = create_response.json()["id"]
    
    # 更新任务
    update_response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "更新后的任务",
            "completed": True
        }
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "更新后的任务"
    assert update_response.json()["completed"] == True