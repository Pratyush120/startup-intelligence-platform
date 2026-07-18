"""
Chart Factory

Reusable Plotly charts for SDIP.
"""

import plotly.express as px


def event_distribution(df):

    if df.empty:
        return None

    fig = px.pie(
        df,
        names="event_type",
        values="total",
        hole=0.55,
        title="Business Event Distribution"
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        legend_title=""
    )

    return fig


def funding_leaderboard(df):

    if df.empty:
        return None

    fig = px.bar(

        df.head(10),

        x="company_name",

        y="amount",

        text="amount",

        title="Top Funding Events"

    )

    fig.update_layout(

        template="plotly_white",

        xaxis_title="",

        yaxis_title="Funding",

        height=420

    )

    return fig


def momentum_chart(df):

    if df.empty:
        return None

    fig = px.bar(

        df,

        x="company_name",

        y="momentum_score",

        color="momentum_score",

        title="Company Momentum"

    )

    fig.update_layout(

        template="plotly_white",

        height=420,

        xaxis_title="",

        yaxis_title="Momentum"

    )

    return fig