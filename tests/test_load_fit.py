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
    # OPEN DESIGN QUESTION (see chat): no broken FIT fixture exists, and
    # hand-authoring FIT bytes isn't practical. Two options:
    #   (a) build a fake `data` dict by hand (e.g. a "running" session with
    #       an incomplete "records" DataFrame missing a required column)
    #       and call check_schema(data) directly -- fastest, no fixture
    #       needed, but bypasses load_session_fit/fitparse entirely
    #   (b) add a real-but-incomplete FIT fixture file and go through
    #       load_session_fit() end-to-end -- more realistic, but requires
    #       producing/sourcing a broken FIT file
    # Once decided, assert pytest.raises(ValueError) is triggered.
    pass
