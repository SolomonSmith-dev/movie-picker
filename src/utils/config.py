"""Configuration management for MoviePicker application."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    tmdb_api_key: str = Field(..., env="TMDB_API_KEY")
    justwatch_api_key: Optional[str] = Field(None, env="JUSTWATCH_API_KEY")
    
    # Database
    database_url: str = Field("sqlite:///./data/moviepicker.db", env="DATABASE_URL")
    
    # Redis
    redis_url: str = Field("redis://localhost:6379", env="REDIS_URL")
    
    # Application
    app_name: str = Field("MoviePicker", env="APP_NAME")
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    # File paths
    data_dir: Path = Field(Path("./data"), env="DATA_DIR")
    movies_dir: Path = Field(Path("./data/movies"), env="MOVIES_DIR")
    logs_dir: Path = Field(Path("./data/logs"), env="LOGS_DIR")
    
    # Web server
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def ensure_directories():
    """Ensure all required directories exist."""
    directories = [
        settings.data_dir,
        settings.movies_dir,
        settings.logs_dir,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_movie_data_path(filename: str) -> Path:
    """Get the full path to a movie data file."""
    return settings.movies_dir / filename


def get_log_file_path(filename: str) -> Path:
    """Get the full path to a log file."""
    return settings.logs_dir / filename 