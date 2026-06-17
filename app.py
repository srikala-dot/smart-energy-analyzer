import streamlit as st
import pandas as pd
from backend import crud, database, models

st.set_page_config(page_title="Energy Platform", layout="wide")
models.Base.metadata.create_all(bind=database.engine)

st.title("⚡ AI-Driven Smart Grid & Energy Analytics")

tab1, tab2 = st.tabs(["📊 Data Management", "🧠 AI Executive Analytics"])

with tab1:
    with st.expander("➕ Add New Log"):
        with st.form("entry_form", clear_on_submit=True):
            f_name = st.text_input("Report Title")
            f_path = st.text_input("Storage Path")
            if st.form_submit_button("Submit"):
                db = database.SessionLocal()
                crud.create_dataset(db, f_name, f_path)
                db.close()
                st.rerun()

    st.subheader("Ingested Telemetry Records")
    db = database.SessionLocal()
    data = crud.get_datasets(db)
    db.close()
    
    if data:
        df = pd.DataFrame([d.__dict__ for d in data]).drop(columns=["_sa_instance_state"], errors='ignore')
        st.dataframe(df, use_container_width=True)
        
        with st.expander("⚠️ Data Governance (Delete Record)"):
            d_id = st.number_input("Target Record ID", min_value=1, step=1)
            # This 'if' acts as the protection gate
            if st.button("Commit Deletion"):
                db = database.SessionLocal()
                crud.delete_dataset(db, int(d_id))
                db.close()
                st.success("Record deleted.")
                st.rerun()
    else:
        st.info("No records to manage.")

with tab2:
    st.subheader("AI Model Selection")
    m = st.tabs(["Linear Regression", "Logistic Classification", "SVM Boundary", "K-Means"])
    m[0].write("### Demand Forecasting Results")
    m[1].write("### Classification Metrics")
    m[2].write("### SVM Boundaries")
    m[3].write("### Cluster Centroids")
