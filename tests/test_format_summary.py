"""
Test suite for format_summary and its formatter functions in summary.py
"""

# -------------------------
# Imports
# -------------------------

import pytest
import pandas as pd
from metrics.summary import format_summary, calc_active_swim_time
from ingestion.load_fit import load_session_fit

# -------------------------
# Test cases
# -------------------------

def test_format_summary_none_value():
    test_summary = {
        "sport": "cycling",
        "avg_power": None
    }
    new_test_summary = format_summary(test_summary)
    assert new_test_summary["avg_power"] == "Not Recorded"


def test_format_summary_timer_time():
    test_summary = {
        "sport": "cycling",
        "timer_time": 10040
    }
    new_test_summary = format_summary(test_summary)
    assert new_test_summary["timer_time"] == "2:47:20"


def test_format_summary_distance_running():
    test_summary = {
        "sport": "running",
        "total_distance": 10.2211
    }
    new_test_summary = format_summary(test_summary)
    assert new_test_summary["total_distance"] == "10.22 mi"


def test_format_summary_distance_swimming():
    test_summary = {
        "sport": "swimming",
        "total_distance": 5000
    }
    new_test_summary = format_summary(test_summary)
    assert new_test_summary["total_distance"] == "5000 yd"


def test_format_summary_pace_running():
    test_summary = {
        "sport": "running",
        "avg_pace": 6.5
    }
    new_test_summary = format_summary(test_summary)
    assert new_test_summary["avg_pace"] == "6:30 min/mi"


def test_format_summary_pace_swimming():
    test_summary = {
        "sport": "swimming",
        "avg_pace": 1.33
    }
    new_test_summary = format_summary(test_summary)
    assert new_test_summary["avg_pace"] == "1:20 min/100yd"


def test_format_summary_unmapped_key_passthrough():
    test_summary = {
        "sport": "running",
    }
    new_test_summary = format_summary(test_summary)
    assert new_test_summary["sport"] == test_summary["sport"]


def test_calc_active_swim_time_filters_idle():
    fake_lengths = {
        "length_type": ["active", "idle", "active", "active", "idle"],
        "total_elapsed_time": [100, 600, 123, 555, 44]
    }
    fake_lengths_df = pd.DataFrame(fake_lengths)
    assert calc_active_swim_time(fake_lengths_df) == 778


def test_calc_active_swim_time_matches_garmin():
    data = load_session_fit("data/raw/test/test_pool_swim.fit")
    active_time = calc_active_swim_time(data["lengths"])
    assert active_time == pytest.approx(3107.262)
