from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Central configuration using Pydantic Settings."""

    # Project
    PROJECT_NAME: str = "Strategic Decision Intelligence Platform"
    VERSION: str = "1.0.0"

    # Environment
    ENVIRONMENT: str = "development"

    # Root directory (resolved relative to this file)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # Database
    DATABASE_PATH: Path = BASE_DIR / "startup_intelligence.db"

    # Data directories
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    EXPORT_DIR: Path = DATA_DIR / "exports"

    # Documentation
    DOCS_DIR: Path = BASE_DIR / "docs"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_DIR: Path = BASE_DIR / "logs"

    # API Keys
    OPENAI_API_KEY: str = ""
    NEWS_API_KEY: str = ""

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # RSS Sources
    GOOGLE_NEWS_RSS: str = (
        "https://news.google.com/rss/search?q=Indian+startup&hl=en-IN&gl=IN&ceid=IN:en"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


Config = Settings()
