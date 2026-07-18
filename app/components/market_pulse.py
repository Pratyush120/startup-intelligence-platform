"""
Market Pulse Component
"""

import streamlit as st


def render_market_pulse(summary):

    st.subheader("🔥 Market Pulse")

    col1, col2 = st.columns(2)

    with col1:

        st.success("Funding Activity")

        st.write("🟢 Strong")

        st.success("Hiring")

        st.write("🟢 Growing")

    with col2:

        st.warning("Layoffs")

        st.write("🟡 Stable")

        st.success("Expansion")

        st.write("🟢 Active")