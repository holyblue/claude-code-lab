"""
Configuration management for the time tracking system.

This module handles loading and validation of configuration from environment variables.
"""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings can be overridden by creating a .env file in the backend directory.
    """

    # Database
    DATABASE_URL: str = "sqlite:///./data/app.db"

    # Application
    APP_NAME: str = "Time Tracking System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Timezone
    TIMEZONE: str = "UTC+8"

    # Work Hours
    STANDARD_WORK_HOURS: float = 7.5
    MAX_WORK_HOURS: float = 12.0
    MIN_TIME_UNIT: float = 0.5

    # Work Days (1=Monday, 7=Sunday)
    WORK_DAYS: List[int] = [1, 2, 3, 4, 5]  # Monday to Friday

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
