import streamlit as st
import pandas as pd
from backend import crud, database, models

# 1. Page Configuration for a professional look
st.set_page_config(page_title="Energy Intelligence Platform", layout="wide")

# 2. Modern UI Styling
st.markdown("""
    <style>
    .stApp {background-color: #f0f2f6;}
    .hero {background-color: #1e1e1e; color: #ffffff; padding: 2rem; border-radius: 15px; margin-bottom: 20px;}
    .metric-card {background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    </style>
""", unsafe_html=True)

# 3. Hero Section (The "Professional First Impression")
st.markdown('<div class="hero"><h1>⚡ Energy Intelligence Platform</h1><p>AI-Driven Analytics for Household Consumption Optimization</p></div>', unsafe_html=True)

# 4. Data Logic
models.Base.metadata.create_all(bind=database.engine)
db = database.SessionLocal()
data = crud.get_datasets(db)
db.close()

# 5. Dashboard Grid
col1, col2, col3 = st.columns(3)
col1.metric("Active Records", len(data) if data else 0, "Current")
col2.metric("System Health", "Online", "Stable")
col3.metric("Analysis Engine", "Active", "Ready")

st.write("---")

# 6. Data Management Section
tab1, tab2 = st.tabs(["📊 Consumption Logs", "➕ Add New Entry"])

with tab1:
    st.subheader("Current Consumption Overview")
    if data:
        df = pd.DataFrame([d.__dict__ for d in data])
        if "_sa_instance_state" in df.columns:
            df = df.drop(columns=["_sa_instance_state"])
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data found. Navigate to the 'Add New Entry' tab to begin.")

with tab2:
    st.subheader("Log New Energy Usage")
    with st.form("new_entry_form"):
        f_name = st.text_input("Dataset Label (e.g., January Usage)")
        f_path = st.text_input("Storage Location/Path")
        submit = st.form_submit_button("Submit to Database")
        if submit:
            db = database.SessionLocal()
            crud.create_dataset(db, filename=f_name, path=f_path)
            db.close()
            st.success("Record successfully logged. Rerun the app to update.")
