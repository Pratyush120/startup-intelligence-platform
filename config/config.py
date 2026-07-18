from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration for the project."""

    # Project
    PROJECT_NAME = "Strategic Decision Intelligence Platform"
    VERSION = "1.0.0"

    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # Root directory
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Data directories
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    EXPORT_DIR = DATA_DIR / "exports"

    # Documentation
    DOCS_DIR = BASE_DIR / "docs"

    # Database
    DATABASE_PATH = BASE_DIR / "startup_intelligence.db"

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = BASE_DIR / "logs"

    # RSS Sources
    GOOGLE_NEWS_RSS = (
    "https://news.google.com/rss/search?q=Indian+startup&hl=en-IN&gl=IN&ceid=IN:en"
)
    

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")