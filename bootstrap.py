"""
Project Bootstrap

Adds the project root to Python's import path.

This allows Streamlit pages to import src, config, etc.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
