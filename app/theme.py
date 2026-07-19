import streamlit as st
from pathlib import Path


def apply_theme():

    st.set_page_config(
        page_title="Strategic Decision Intelligence Platform",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    css = Path(__file__).parent / "assets" / "styles.css"

    with open(css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
