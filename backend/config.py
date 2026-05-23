"""Configuration settings for the Exhibit Packet Builder backend."""

from typing import Optional
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Application settings."""
    
    # App
    APP_NAME: str = "Exhibit Packet Builder"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./exhibit_builder.db"
    # For production: postgresql://user:password@localhost/db_name
    
    # File Upload
    UPLOAD_DIR: Path = Path("uploads")
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: set = {
        "pdf", "doc", "docx", "txt", "jpg", "jpeg", "png", "tiff", "tif", "gif", "bmp"
    }
    
    # Processing
    TEMP_DIR: Path = Path("temp")
    OCR_ENABLED: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
