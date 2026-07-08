# Partner Catalog Processor

A Streamlit app that lets a user upload a Partner Catalog workbook, identify inactive UPC rows, set their Price to 0, and download the updated spreadsheet.

## What this project is built for

This repo is structured so the core workbook-processing logic stays separate from Streamlit. That keeps the app easy to maintain now and makes a future API or FAST integration easier later.

## Project structure

- `app.py` - Streamlit UI
- `src/catalog_processor.py` - reusable workbook-processing logic
- `src/__init__.py` - package marker
- `tests/test_catalog_processor.py` - unit tests
- `requirements.txt` - Python dependencies

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How it works

1. Upload a Partner Catalog `.xlsx` file.
2. Choose the worksheet.
3. The app looks for a Price column and a Status/Active column.
4. Rows marked inactive are updated so Price becomes `0`.
5. Download the updated workbook.

## Notes

- Manual column overrides are available when headers do not match the defaults.
- The processing code is isolated in `src/catalog_processor.py` so another interface can reuse it later.
- The current output is the same Partner Catalog workbook, updated in place.
