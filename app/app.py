"""
Strategic Decision Intelligence Platform

Dashboard Entry Point
"""

import sys
from pathlib import Path

# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --------------------------------------------------

import streamlit as st

from theme import apply_theme
from components.sidebar import render_sidebar

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

apply_theme()

render_sidebar()

# --------------------------------------------------
# Home Page
# --------------------------------------------------

st.title("📈 Strategic Decision Intelligence Platform")

st.markdown(
"""
Welcome to the Strategic Decision Intelligence Platform.

This platform collects startup news, extracts business events,
builds company intelligence, and provides executive dashboards
for strategic decision making.
"""
)

st.markdown("---")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("📰 News Collection")

with c2:
    st.success("🧠 Intelligence Engine")

with c3:
    st.warning("📊 Business Dashboard")

st.markdown("---")

st.subheader("Platform Modules")

st.markdown("""
- 📊 Executive Overview
- 🏢 Company Intelligence
- 📰 Business Events
- 📄 Executive Reports
- 📈 Analytics
""")

st.success("Use the navigation menu on the left to explore the platform.")