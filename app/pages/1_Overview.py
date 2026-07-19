"""
Overview Dashboard
"""
# ruff: noqa: E402

# -------------------------------------------------------
# Bootstrap
# -------------------------------------------------------

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# -------------------------------------------------------

import streamlit as st

from src.analytics.dashboard_analytics import DashboardAnalytics
from app.components.cards import metric_card
from app.components.tables import show_dataframe
from app.components.charts import event_distribution_chart

# -------------------------------------------------------
# Load Dashboard Data
# -------------------------------------------------------

analytics = DashboardAnalytics()

dashboard = analytics.overview()

summary = dashboard["summary"]

companies = dashboard["companies"]

events = dashboard["events"]

distribution = dashboard["distribution"]

funding = dashboard["funding"]

# -------------------------------------------------------
# PAGE
# -------------------------------------------------------

st.title("📊 Executive Dashboard")

st.caption("Strategic Decision Intelligence Platform")

st.divider()

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card(
        "Business Events",
        summary["total_events"]
    )

with c2:
    metric_card(
        "Companies",
        summary["total_companies"]
    )

with c3:

    funding_value = summary["total_funding"]

    metric_card(
        "Funding",
        f"${funding_value:,.0f}"
    )

with c4:
    metric_card(
        "Avg Confidence",
        f"{summary['avg_confidence']:.2f}"
    )

st.divider()

# -------------------------------------------------------
# Main Layout
# -------------------------------------------------------

left, right = st.columns([2, 1])

# -------------------------------------------------------

with left:

    st.subheader("🏆 Top Companies")

    show_dataframe(companies)

    st.markdown("")

    st.subheader("📰 Recent Business Events")

    show_dataframe(events)

# -------------------------------------------------------

with right:

    st.subheader("📊 Event Distribution")

    fig = event_distribution_chart(distribution)

    if fig:

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("")

    st.subheader("💰 Largest Funding Events")

    show_dataframe(funding)

analytics.close()