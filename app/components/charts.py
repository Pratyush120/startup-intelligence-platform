"""
Reusable Plotly Charts
"""

import plotly.express as px


def event_distribution_chart(df):

    if df.empty:
        return None

    fig = px.bar(
        df, x="event_type", y="total", text="total", title="Business Event Distribution"
    )

    fig.update_layout(
        template="plotly_white", height=450, xaxis_title="", yaxis_title="Events"
    )

    return fig
