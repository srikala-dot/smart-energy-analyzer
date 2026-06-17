import streamlit as st
import pandas as pd
from backend import crud, database, models, ml_models # Import your new ml_models

st.set_page_config(page_title="Energy Platform", layout="wide")
models.Base.metadata.create_all(bind=database.engine)

st.title("⚡ AI-Driven Energy Analytics")

tab1, tab2 = st.tabs(["📊 Data Management", "🧠 AI Executive Analytics"])

with tab1:
    # ... (Your existing ingestion and delete logic) ...
    with st.expander("⚠️ Data Governance"):
        d_id = st.number_input("Delete Record ID", min_value=1, step=1)
        if st.button("Commit Deletion"):
            db = database.SessionLocal()
            crud.delete_dataset(db, int(d_id)) # Corrected function call
            db.close()
            st.rerun()

with tab2:
    st.subheader("Model Selection Panel")
    # This renders the tabs for your models
    model_tabs = st.tabs(["Linear Regression", "Logistic Classification", "SVM Boundary", "K-Means"])
    
    # We use a dummy dataframe for demonstration
    dummy_data = pd.DataFrame({'val': [1, 2, 3]}) 

    with model_tabs[0]:
        st.write(ml_models.run_linear_regression(dummy_data))
    with model_tabs[1]:
        st.write(ml_models.run_logistic_classification(dummy_data))
    with model_tabs[2]:
        st.write(ml_models.run_svm(dummy_data))
    with model_tabs[3]:
        st.write(ml_models.run_kmeans(dummy_data))
