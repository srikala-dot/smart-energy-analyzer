import streamlit as st
import pandas as pd
from backend import crud, database, models

# 1. Setup the page
st.set_page_config(page_title="Energy Dashboard", layout="wide")

# 2. Create the table structure in the database if it's missing
models.Base.metadata.create_all(bind=database.engine)

st.title("⚡ Smart Energy Analytics Platform")

# 3. Connect to database and fetch data
db = database.SessionLocal()
data = crud.get_datasets(db)
db.close()

# 4. Display the data
st.subheader("Household Energy Consumption Data")
if data:
    df = pd.DataFrame([d.__dict__ for d in data])
    # Removing internal database columns to keep it clean
    if "_sa_instance_state" in df.columns:
        df = df.drop(columns=["_sa_instance_state"])
    st.table(df)
else:
    st.write("The database is connected, but no data has been added yet.")
    st.info("Tip: Add some energy records to see them appear here.")
