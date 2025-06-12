from fastapi import HTTPException, Request, FastAPI
from fastapi.responses import JSONResponse

class TaskNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Task not found")

def create_exception_handlers(app: FastAPI):
    @app.exception_handler(TaskNotFoundException)
    async def task_not_found_handler(request: Request, exc: TaskNotFoundException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )