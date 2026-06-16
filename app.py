import streamlit as st
import pandas as pd
from backend import crud, database, models

# 1. Professional Page Setup
st.set_page_config(page_title="Energy Intelligence Platform", layout="centered")

# 2. Hero Header
st.title("⚡ Energy Intelligence Platform")
st.markdown("---")

# 3. Database Logic
models.Base.metadata.create_all(bind=database.engine)
db = database.SessionLocal()
data = crud.get_datasets(db)
db.close()

# 4. Interactive Sections
st.subheader("📊 Dashboard Controls")

# Create a clean layout for the user
tab1, tab2 = st.tabs(["📑 View Records", "➕ Add New Log"])

with tab1:
    st.info(f"You currently have {len(data) if data else 0} saved energy records.")
    if data:
        df = pd.DataFrame([d.__dict__ for d in data])
        if "_sa_instance_state" in df.columns:
            df = df.drop(columns=["_sa_instance_state"])
        st.dataframe(df, use_container_width=True)

with tab2:
    st.write("Fill in the details below to add a new energy report to the system.")
    with st.form("entry_form", clear_on_submit=True):
        # Professional labels with help text
        f_name = st.text_input("Report Title", help="Give this energy report a unique name (e.g., 'May 2026 Power Usage')")
        f_path = st.text_input("Storage Location/Path", help="Enter the file path where your raw data is stored")
        
        submit = st.form_submit_button("🚀 Submit to Database")
        if submit:
            if f_name and f_path:
                db = database.SessionLocal()
                crud.create_dataset(db, filename=f_name, path=f_path)
                db.close()
                st.success(f"Successfully saved '{f_name}'!")
            else:
                st.error("Please fill in both fields.")
