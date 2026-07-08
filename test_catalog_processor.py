from src.catalog_processor import process_catalog
import pandas as pd

def test_process():
    assert not process_catalog(pd.DataFrame()).empty==False
