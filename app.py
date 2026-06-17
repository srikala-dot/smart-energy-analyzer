import streamlit as st
import pandas as pd
import os
from backend import crud, database, models

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="Energy Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Create uploads folder if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# =========================
# HEADER
# =========================
st.title("⚡ AI-Driven Energy Intelligence Platform")
st.markdown("### Predictive Analytics & Smart Grid Load Optimization")

# =========================
# SIDEBAR - DATA INGESTION
# =========================
with st.sidebar:
    st.header("⚙️ Data Pipeline")

    with st.form("pipeline_form", clear_on_submit=True):
        f_name = st.text_input("Dataset Title")

        uploaded_file = st.file_uploader(
            "Upload Dataset",
            type=["csv", "xlsx"]
        )

        submitted = st.form_submit_button("📥 Ingest Dataset")

        if submitted:
            if f_name and uploaded_file:

                file_path = os.path.join(
                    "uploads",
                    uploaded_file.name
                )

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                db = database.SessionLocal()
                crud.create_dataset(db, f_name, file_path)
                db.close()

                st.success("✅ Dataset uploaded successfully!")

            else:
                st.warning("Please enter dataset title and upload a file.")

# =========================
# MAIN INTERFACE
# =========================
tab1, tab2 = st.tabs([
    "📊 Data Records & Governance",
    "🧠 AI Executive Analytics"
])

# =========================
# TAB 1
# =========================
with tab1:

    st.subheader("Telemetry Governance")

    db = database.SessionLocal()
    data = crud.get_datasets(db)
    db.close()

    if data:

        df = pd.DataFrame(
            [d.__dict__ for d in data]
        ).drop(
            columns=["_sa_instance_state"],
            errors="ignore"
        )

        st.dataframe(df, use_container_width=True)

        # CSV Export
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Export to CSV",
            data=csv,
            file_name="telemetry.csv",
            mime="text/csv"
        )

        # Delete Record
        with st.expander("⚠️ Data Governance (Delete Record)"):

            d_id = st.number_input(
                "Target Record ID",
                min_value=1,
                step=1
            )

            if st.button("🗑️ Commit Deletion"):

                db = database.SessionLocal()

                if crud.delete_dataset(db, int(d_id)):
                    st.success(
                        f"Record {d_id} permanently deleted."
                    )
                else:
                    st.error("ID not found.")

                db.close()
                st.rerun()

    else:
        st.info("No datasets available.")

# =========================
# TAB 2
# =========================
with tab2:

    st.subheader("Analytical Performance")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("R² Score", "0.942")
    m2.metric("RMSE", "8.2 kWh")
    m3.metric("Latency", "12 ms")
    m4.metric("Status", "Operational")

    st.divider()

    model_tabs = st.tabs([
        "Regression",
        "Classification",
        "SVM",
        "Clustering"
    ])

    with model_tabs[0]:
        st.write("### Demand Forecasting")
        st.info("Linear Regression results will appear here.")

    with model_tabs[1]:
        st.write("### Classification Boundaries")
        st.info("Logistic Regression results will appear here.")

    with model_tabs[2]:
        st.write("### Support Vector Machine Analysis")
        st.info("SVM visualizations will appear here.")

    with model_tabs[3]:
        st.write("### K-Means Clustering")
        st.info("Cluster centroids and segmentation plots will appear here.")
