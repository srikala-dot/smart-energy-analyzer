import streamlit as st
from backend import crud, database

# Executive Presentation Configuration
st.set_page_config(
    page_title="AI-Driven Smart Grid & Household Energy Analytics Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Smart Energy Analytics Platform")
st.write("Dashboard is loading...")
