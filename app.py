import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="PC Validation", layout="wide")

st.title("PC Validation")
st.write("Upload a Partner Catalog spreadsheet to preview it and process updates.")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Choose a sheet", xls.sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

        st.subheader("Preview")
        st.dataframe(df.head(20), use_container_width=True)

        st.info("Next step: add the logic to identify inactive UPCs and set Price to 0.")

        if st.button("Process file"):
            st.success("File loaded successfully. Processing logic will go here.")
    except Exception as e:
        st.error(f"Could not read file: {e}")
