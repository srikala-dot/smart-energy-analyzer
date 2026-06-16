import streamlit as st
import pandas as pd
from backend import crud, database

# 1. Setup the page
st.set_page_config(page_title="Energy Dashboard", layout="wide")
st.title("⚡ Smart Energy Analytics Platform")

# 2. Connect to the database
# We call the session from your database file
db = database.SessionLocal()

# 3. Fetch data using your crud file
# Assuming you have a function named 'get_all_data' in your crud.py
data = crud.get_all_data(db)

# 4. Display the data
st.subheader("Household Energy Consumption Data")
if data:
    df = pd.DataFrame(data)
    st.table(df)
else:
    st.write("No data found in the database yet.")

# Close the database connection
db.close()
