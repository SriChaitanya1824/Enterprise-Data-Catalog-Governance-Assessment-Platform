"""Application configuration."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/catalog_db"
    
    # JWT
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # OpenLineage
    OPENLINEAGE_URL: Optional[str] = None
    MARQUEZ_URL: Optional[str] = None
    
    # Application
    APP_NAME: str = "Enterprise Data Catalog & Governance Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()
