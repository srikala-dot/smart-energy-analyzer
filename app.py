import streamlit as st
import pandas as pd
from backend import crud, database, models

# 1. Page Configuration
st.set_page_config(page_title="Smart Energy Analytics", layout="wide")

# 2. Custom Dark Theme CSS (Makes it look professional)
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    .stMetric {background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333;}
    h1 {color: #00f2ff;}
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar for Data Entry (Like the "Get Started" / "Account" sections)
with st.sidebar:
    st.header("⚙️ Data Input")
    with st.form("input_form"):
        f_name = st.text_input("File Name")
        f_path = st.text_input("File Path")
        submit = st.form_submit_button("Submit Data")
        if submit:
            db = database.SessionLocal()
            crud.create_dataset(db, filename=f_name, path=f_path)
            db.close()
            st.success("Data successfully recorded!")
            st.rerun()

# 4. Hero Section
st.title("⚡ Smart Energy Analytics Platform")
st.subheader("Leverage AI to predict consumption and optimize your efficiency.")

# 5. Metric Cards (Professional Grid)
models.Base.metadata.create_all(bind=database.engine)
db = database.SessionLocal()
data = crud.get_datasets(db)
db.close()

col1, col2, col3 = st.columns(3)
col1.metric("Total Datasets", len(data) if data else 0, "Active")
col2.metric("System Status", "Operational", "Stable")
col3.metric("AI Model", "Enabled", "Active")

st.write("---")

# 6. Data Visualization Table
st.subheader("Detailed Consumption Logs")
if data:
    df = pd.DataFrame([d.__dict__ for d in data])
    if "_sa_instance_state" in df.columns:
        df = df.drop(columns=["_sa_instance_state"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("Awaiting input data. Use the sidebar to add your first energy record.")
    
