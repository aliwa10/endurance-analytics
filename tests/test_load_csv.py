"""
Test suite for load_session_csv function in load_csv.py
"""

# -------------------------
# Imports
# -------------------------

import pytest
from pathlib import Path
import pandas as pd
from ingestion.load_csv import load_session_csv

# -------------------------
# Test cases
# -------------------------

def test_load_valid_csv():
    test_df = load_session_csv("data/raw/test/test_session.csv")
    assert isinstance(test_df, pd.DataFrame)
    assert list(test_df.columns) == ["time", "heart_rate", "power"]
    assert len(test_df) == 4

def test_load_missing_file():
    with pytest.raises(FileNotFoundError):
        load_session_csv("nonexistent.csv")

def test_load_malformed_csv():
    with pytest.raises(pd.errors.ParserError):
        load_session_csv("data/raw/test/test_session_malformed.csv")
