"""
News Feed Cards
"""

import streamlit as st


def render_news_feed(df):

    st.subheader("📰 Latest Intelligence")

    if df.empty:

        st.info("No events detected.")

        return

    for _, row in df.head(5).iterrows():

        with st.container():

            st.markdown(

                f"""
### {row['event_type']}

**{row['company_name']}**

{row['title']}

Confidence : **{row['confidence']}**

Impact : **{row['impact_score']}**
                """

            )

            st.divider()