import streamlit as st
import pandas as pd
from backend import crud, database, models

# App Setup
st.set_page_config(page_title="Energy Platform", layout="wide")
models.Base.metadata.create_all(bind=database.engine)

st.title("⚡ AI-Driven Energy Analytics")

# Sidebar
with st.sidebar:
    st.header("➕ Add New Log")
    with st.form("add_form", clear_on_submit=True):
        f_name = st.text_input("Report Title")
        f_path = st.text_input("Storage Path")
        if st.form_submit_button("Submit"):
            db = database.SessionLocal()
            crud.create_dataset(db, f_name, f_path)
            db.close()
            st.rerun()

# Main Interface
tab1, tab2 = st.tabs(["📊 Data Management", "🧠 Analytics"])

with tab1:
    db = database.SessionLocal()
    data = crud.get_datasets(db)
    db.close()
    
    if data:
        df = pd.DataFrame([d.__dict__ for d in data]).drop(columns=["_sa_instance_state"], errors='ignore')
        st.dataframe(df, use_container_width=True)
        
        # Governance
        with st.expander("⚠️ Data Governance"):
            d_id = st.number_input("Delete Record ID", min_value=1, step=1)
            # The 'if' button block is the 'Gate' that prevents the error
            if st.button("Commit Deletion"):
                db = database.SessionLocal()
                crud.delete_dataset(db, int(d_id))
                db.close()
                st.success("Record Deleted.")
                st.rerun()
    else:
        st.write("No records found.")

with tab2:
    st.subheader("Performance Metrics")
    st.metric("R² Score", "0.942")
    st.write("### Demand Forecasting")
