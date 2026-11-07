"""Authenticated task CRUD endpoints."""
from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlalchemy import select
from app.dependencies import CurrentUser, DatabaseSession
from app.models import Task
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: DatabaseSession, current_user: CurrentUser) -> Task:
    task = Task(**task_data.model_dump(), owner_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("", response_model=list[TaskResponse])
def list_tasks(db: DatabaseSession, current_user: CurrentUser, status_filter: str | None = Query(default=None, alias="status"), search: str | None = Query(default=None, min_length=1, max_length=150), skip: int = Query(default=0, ge=0), limit: int = Query(default=20, ge=1, le=100)) -> list[Task]:
    statement = select(Task).where(Task.owner_id == current_user.id)
    if status_filter:
        statement = statement.where(Task.status == status_filter)
    if search:
        statement = statement.where(Task.title.ilike(f"%{search}%"))
    statement = statement.order_by(Task.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(statement).all())

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: DatabaseSession, current_user: CurrentUser) -> Task:
    task = db.scalar(select(Task).where(Task.id == task_id, Task.owner_id == current_user.id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: DatabaseSession, current_user: CurrentUser) -> Task:
    task = db.scalar(select(Task).where(Task.id == task_id, Task.owner_id == current_user.id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: DatabaseSession, current_user: CurrentUser) -> Response:
    task = db.scalar(select(Task).where(Task.id == task_id, Task.owner_id == current_user.id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
