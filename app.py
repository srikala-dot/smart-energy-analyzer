import streamlit as st
import pandas as pd
from backend import crud, database, models

# Setup
models.Base.metadata.create_all(bind=database.engine)

st.set_page_config(page_title="Energy Intelligence Platform", layout="wide")
st.title("⚡ AI-Driven Smart Grid & Energy Analytics")

# Sidebar
with st.sidebar:
    st.header("➕ Add New Log")
    with st.form("entry_form", clear_on_submit=True):
        f_name = st.text_input("Report Title")
        f_path = st.text_input("Storage Location/Path")
        if st.form_submit_button("🚀 Submit"):
            db = database.SessionLocal()
            crud.create_dataset(db, filename=f_name, path=f_path)
            db.close()
            st.rerun()

# Main Tabs
tab1, tab2 = st.tabs(["📑 View Records", "📈 Analytics"])

with tab1:
    db = database.SessionLocal()
    data = crud.get_datasets(db)
    db.close()
    
    if data:
        df = pd.DataFrame([d.__dict__ for d in data]).drop(columns=["_sa_instance_state"], errors='ignore')
        st.dataframe(df, use_container_width=True)
        
        # Delete section
        with st.expander("🗑️ Delete a Record"):
            del_id = st.number_input("Enter ID", min_value=1, step=1)
            if st.button("Confirm Delete"):
                db = database.SessionLocal()
                crud.delete_dataset(db, del_id)
                db.close()
                st.rerun()

with tab2:
    st.write("### AI Model Operations")
    st.info("System is ready for telemetry streams.")
