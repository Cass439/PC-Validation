from __future__ import annotations

from io import BytesIO

import pandas as pd
import streamlit as st

from src.catalog_processor import CatalogProcessingError, process_workbook

st.set_page_config(page_title="PC Validation", page_icon="📘", layout="wide")

st.title("PC Validation")
st.caption(
    "Upload a Partner Catalog workbook plus the zero-sales CSV, then set Price = 0 for GTINs that match BARCODE rows where TOTAL_SALES is 0."
)

catalog_file = st.file_uploader("Upload Partner Catalog (.xlsx)", type=["xlsx"])
sales_file = st.file_uploader("Upload zero-sales file (.csv)", type=["csv"])

if not catalog_file or not sales_file:
    st.info("Upload both files to continue.")
    st.stop()

catalog_bytes = catalog_file.getvalue()
sales_bytes = sales_file.getvalue()

preview_col1, preview_col2 = st.columns(2)
with preview_col1:
    st.subheader("Partner Catalog preview")
    try:
        catalog_preview = pd.read_excel(BytesIO(catalog_bytes), sheet_name=0, nrows=10)
        st.dataframe(catalog_preview, use_container_width=True)
    except Exception as exc:
        st.error(f"Could not preview the Partner Catalog: {exc}")
        st.stop()

with preview_col2:
    st.subheader("Sales CSV preview")
    try:
        sales_preview = pd.read_csv(BytesIO(sales_bytes)).head(10)
        st.dataframe(sales_preview, use_container_width=True)
    except Exception as exc:
        st.error(f"Could not preview the sales CSV: {exc}")
        st.stop()

process_clicked = st.button("Process files", type="primary")

if process_clicked:
    try:
        output_bytes, report = process_workbook(
            catalog_bytes=catalog_bytes,
            sales_csv_bytes=sales_bytes,
        )
    except CatalogProcessingError as exc:
        st.error(str(exc))
        st.stop()
    except Exception as exc:
        st.error(f"Unexpected error: {exc}")
        st.stop()

    st.success(
        f"Matched {report.matched_rows} GTIN rows and updated Price on {report.updated_rows} rows."
    )

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Catalog rows processed", report.total_rows)
    metric2.metric("Matched GTIN rows", report.matched_rows)
    metric3.metric("Price updates", report.updated_rows)

    st.write("Detected columns")
    st.code(
        f"Sheet: {report.sheet_name}\nGTIN: {report.gtin_column}\nPrice: {report.price_column}\nSales barcode column: {report.barcode_column}\nSales value column: {report.sales_column}"
    )

    st.download_button(
        label="Download updated Partner Catalog",
        data=output_bytes,
        file_name=catalog_file.name.replace(".xlsx", "_updated.xlsx"),
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
