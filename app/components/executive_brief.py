"""
Executive Brief Generator
"""

import streamlit as st


def render_executive_brief(summary):

    st.subheader("📄 Executive Brief")

    text = f"""

Funding activity remains positive.

The platform detected **{summary["total_events"]}**

business events involving

**{summary["total_companies"]} companies**.

Overall confidence remains high

at **{summary["avg_confidence"]}**.

Investment sentiment remains positive.
"""

    st.info(text)
