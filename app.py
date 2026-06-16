import streamlit as st
import pandas as pd
from backend import crud, database, models

# 1. Page Configuration
st.set_page_config(page_title="Energy Intelligence Platform", layout="wide")

# 2. Hero Section
st.title("⚡ Energy Intelligence Platform")
st.subheader("AI-Driven Analytics for Household Consumption")

# 3. Database Setup
models.Base.metadata.create_all(bind=database.engine)
db = database.SessionLocal()
data = crud.get_datasets(db)
db.close()

# 4. Metrics Grid
col1, col2, col3 = st.columns(3)
col1.metric("Active Records", len(data) if data else 0)
col2.metric("System Status", "Online")
col3.metric("Analysis Engine", "Ready")

st.write("---")

# 5. Tabs for Data Management
tab1, tab2 = st.tabs(["📊 Consumption Logs", "➕ Add New Entry"])

with tab1:
    st.subheader("Current Consumption Overview")
    if data:
        df = pd.DataFrame([d.__dict__ for d in data])
        if "_sa_instance_state" in df.columns:
            df = df.drop(columns=["_sa_instance_state"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No data found. Use the 'Add New Entry' tab to begin.")

with tab2:
    st.subheader("Log New Energy Usage")
    with st.form("new_entry_form", clear_on_submit=True):
        f_name = st.text_input("Dataset Label")
        f_path = st.text_input("Storage Location/Path")
        submit = st.form_submit_button("Submit to Database")
        if submit:
            db = database.SessionLocal()
            crud.create_dataset(db, filename=f_name, path=f_path)
            db.close()
            st.success("Record added! Refresh the page to see changes.")
