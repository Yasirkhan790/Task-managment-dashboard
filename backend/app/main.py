"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Task Management API", description="A learning-focused REST API with user accounts and task management.", version="1.0.0", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/", tags=["Health"])
def root() -> dict[str, str]:
    return {"message": "Task Management API is running"}

@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
