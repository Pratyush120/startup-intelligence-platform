"""
Dashboard Layout

Assembles all dashboard components into the Executive Dashboard.
"""

import streamlit as st

from app.components.header import render_header
from app.components.metric_cards import metric_grid
from app.components.executive_brief import render_executive_brief
from app.components.market_pulse import render_market_pulse
from app.components.leaderboard import render_leaderboard
from app.components.news_cards import render_news_feed
from app.components.chart_factory import (
    event_distribution,
    momentum_chart,
)


def render_dashboard(data):

    summary = data["summary"]

    companies = data["companies"]

    events = data["events"]

    distribution = data["distribution"]

    # ---------------------------------------------------

    render_header()

    # ---------------------------------------------------

    metric_grid(summary)

    st.divider()

    render_executive_brief(summary)

    st.divider()

    render_market_pulse(summary)

    st.divider()

    left, right = st.columns(2)

    with left:
        fig = momentum_chart(companies)

        if fig:
            st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = event_distribution(distribution)

        if fig:
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    left, right = st.columns([1, 2])

    with left:
        render_leaderboard(companies)

    with right:
        render_news_feed(events)
