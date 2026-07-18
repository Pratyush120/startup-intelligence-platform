"""
Reusable Tables
"""

import streamlit as st


def show_dataframe(df):

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )