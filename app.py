import streamlit as st
import pandas as pd
from backend import crud, database, models

# 1. Page Config
st.set_page_config(page_title="Energy Intelligence Platform", layout="centered")

# 2. Header
st.title("⚡ Energy Intelligence Platform")
st.markdown("---")

# 3. Database Setup
models.Base.metadata.create_all(bind=database.engine)
db = database.SessionLocal()
data = crud.get_datasets(db)
db.close()

# 4. User Guide Section
with st.expander("ℹ️ How to use this platform"):
    st.write("""
    1. **Add New Log:** Click the 'Add New Log' tab to input your energy usage details. 
    2. **Submit:** Fill in the title and path, then click 'Submit to Database'.
    3. **View Records:** Navigate to the 'View Records' tab to see your saved data.
    4. **Export:** Use the download button below the table to save your reports as CSV.
    """)

# 5. Dashboard Summary
c1, c2, c3 = st.columns(3)
c1.metric("Total Records", len(data) if data else 0)
c2.metric("System", "Online")
c3.metric("DB Status", "Connected")

# 6. Tabs
tab1, tab2 = st.tabs(["➕ Add New Log", "📑 View Records"])

with tab1:
    st.subheader("Log New Energy Usage")
    with st.form("entry_form", clear_on_submit=True):
        f_name = st.text_input("Report Title")
        f_path = st.text_input("Storage Location/Path")
        if st.form_submit_button("🚀 Submit to Database"):
            if f_name and f_path:
                db = database.SessionLocal()
                crud.create_dataset(db, filename=f_name, path=f_path)
                db.close()
                st.success(f"Successfully saved '{f_name}'!")
            else:
                st.error("Please fill in all fields.")

with tab2:
    st.subheader("Stored Consumption Logs")
    if data:
        df = pd.DataFrame([d.__dict__ for d in data])
        if "_sa_instance_state" in df.columns:
            df = df.drop(columns=["_sa_instance_state"])
        st.dataframe(df, use_container_width=True)
        # Download Button
        csv = df.to_csv(index=False)
        st.download_button("📥 Download Logs as CSV", csv, "energy_logs.csv")
    else:
        st.info("No records found yet.")
