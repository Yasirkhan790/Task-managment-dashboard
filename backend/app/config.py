"""Application configuration loaded from environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Settings used throughout the application."""
    secret_key: str = "local-development-key-change-before-deployment"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./task_manager.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
