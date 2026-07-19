# ruff: noqa: E402
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analytics.dashboard_analytics import DashboardAnalytics

from app.components.dashboard_layout import render_dashboard


analytics = DashboardAnalytics()

dashboard = analytics.overview()

render_dashboard(dashboard)

analytics.close()
