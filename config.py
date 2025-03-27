from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Resume Classifier API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for classifying whether a document is a resume or not"
    
    # CORS Settings
    ALLOWED_HOSTS: list[str] = ["*"]  # In production, replace with specific domains
    
    # Security Settings
    API_KEY: str = "your-secret-key-here"  # In production, use environment variable
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set[str] = {'.pdf', '.docx', '.txt'}
    
    # Model Settings
    MODEL_PATH: str = "training_data"
    
    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
