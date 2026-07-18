"""
Professional KPI Cards

Reusable dashboard metric cards.
"""

import streamlit as st


def metric_card(
    title: str,
    value,
    delta=None,
    help_text=None
):
    """
    Render one KPI metric.
    """

    st.metric(

        label=title,

        value=value,

        delta=delta,

        help=help_text

    )


def metric_grid(summary: dict):
    """
    Render the four executive KPI cards.
    """

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        metric_card(

            "📊 Business Events",

            summary["total_events"]

        )

    with c2:

        metric_card(

            "🏢 Companies",

            summary["total_companies"]

        )

    with c3:

        funding = summary["total_funding"]

        metric_card(

            "💰 Total Funding",

            f"${funding:,.0f}"

        )

    with c4:

        metric_card(

            "🎯 Avg Confidence",

            f"{summary['avg_confidence']:.2f}"

        )