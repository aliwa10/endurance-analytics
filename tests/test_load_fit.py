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
# Fixture paths
# -------------------------

RUNNING_FIT_PATH = "data/raw/test/test_run.fit"
CYCLING_FIT_PATH = "data/raw/test/test_bike.fit"
SWIMMING_FIT_PATH = "data/raw/test/test_pool_swim.fit"

# -------------------------
# Test cases
# -------------------------

def test_load_valid_running_fit():
    test_dict = load_session_fit(RUNNING_FIT_PATH)

    assert isinstance(test_dict, dict)
    assert set(test_dict.keys()) == {"session", "laps", "records", "lengths"}
    assert all(isinstance(df, pd.DataFrame) for df in test_dict.values())

    assert all(col in test_dict["records"].columns
        for col in REQUIRED_COLUMNS["running"]["records"])

    assert all(col in test_dict["session"].columns
        for col in REQUIRED_COLUMNS["running"]["session"])

    assert len(test_dict["records"]) > 0


def test_load_valid_cycling_fit():
    test_dict = load_session_fit(CYCLING_FIT_PATH)

    assert isinstance(test_dict, dict)
    assert set(test_dict.keys()) == {"session", "laps", "records", "lengths"}
    assert all(isinstance(df, pd.DataFrame) for df in test_dict.values())

    assert all(col in test_dict["records"].columns
        for col in REQUIRED_COLUMNS["cycling"]["records"])

    assert all(col in test_dict["session"].columns
        for col in REQUIRED_COLUMNS["cycling"]["session"])

    assert len(test_dict["records"]) > 0


def test_load_valid_swimming_fit():
    test_dict = load_session_fit(SWIMMING_FIT_PATH)

    assert isinstance(test_dict, dict)
    assert set(test_dict.keys()) == {"session", "laps", "records", "lengths"}
    assert all(isinstance(df, pd.DataFrame) for df in test_dict.values())

    assert all(col in test_dict["records"].columns
        for col in REQUIRED_COLUMNS["swimming"]["records"])

    assert all(col in test_dict["lengths"].columns
        for col in REQUIRED_COLUMNS["swimming"]["lengths"])

    assert all(col in test_dict["session"].columns
        for col in REQUIRED_COLUMNS["swimming"]["session"])

    assert len(test_dict["lengths"]) > 0


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
