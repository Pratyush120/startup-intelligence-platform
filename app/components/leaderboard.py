"""
Top Companies Leaderboard
"""

import streamlit as st


def render_leaderboard(df):

    st.subheader("🏆 Top Companies")

    if df.empty:
        st.info("No companies available.")

        return

    medals = ["🥇", "🥈", "🥉"]

    for index, (_, row) in enumerate(df.iterrows()):
        medal = medals[index] if index < 3 else "⭐"

        with st.container():
            st.markdown(
                f"""
### {medal} {row["company_name"]}

Momentum : **{row["momentum_score"]}**

Funding : **{row["latest_funding"]}**
                """
            )

            st.divider()
