"""
Test suite for load_session_fit function in load_fit.py
"""

# -------------------------
# Imports
# -------------------------

import pytest
from pathlib import Path
import pandas as pd
from ingestion.load_fit import load_session_fit
from ingestion.validate_schema import check_schema, REQUIRED_COLUMNS

# -------------------------
# Fixture path
# -------------------------

# Real running FIT file (see data/raw/test/test_run.fit). No cycling/swim
# fixtures yet -- add cases for those sports once those files exist.
TEST_FIT_PATH = "data/raw/test/test_run.fit"

# -------------------------
# Test cases
# -------------------------

def test_load_valid_fit():
    test_dict = load_session_fit(TEST_FIT_PATH)
    assert isinstance(test_dict, dict)
    assert set(test_dict.keys()) == {"session", "laps", "records", "lengths"}
    for key in test_dict:
        assert isinstance(test_dict[key], pd.DataFrame)
    for col in REQUIRED_COLUMNS["running"]["records"]:
        assert col in test_dict["records"].columns
    assert len(test_dict["records"]) > 0

def test_load_missing_file():
    with pytest.raises(FileNotFoundError):
        load_session_fit("nonexistent.fit")

def test_schema_validation_failure():
    fake_data = {
        "session": pd.DataFrame({"sport": ["running"]}),
        "records": pd.DataFrame({"timestamp": [1], "distance": [1]})
    }
    with pytest.raises(ValueError):
        check_schema(fake_data)
