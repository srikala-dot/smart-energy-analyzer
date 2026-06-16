import streamlit as st
import pandas as pd
import numpy as np
import os
import seaborn as sns

# Import directly from the backend package
from backend import crud, database

# Executive Presentation Configuration
st.set_page_config(
    page_title="AI-Driven Smart Grid & Household Energy Analytics Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional UI Styling
st.markdown("""
<style>
    .main { background-color: #f5f5f5; }
</style>
""", unsafe_allow_html=True)

st.title("Smart Energy Analytics Platform")
st.write("Welcome to your dashboard!")
