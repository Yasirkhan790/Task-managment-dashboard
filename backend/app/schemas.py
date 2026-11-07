"""Pydantic request and response schemas."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models import TaskStatus

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=5000)
    status: TaskStatus = TaskStatus.TODO
    due_date: datetime | None = None

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=5000)
    status: TaskStatus | None = None
    due_date: datetime | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
