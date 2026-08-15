"""
Test suite for format_summary and its formatter functions in summary.py
"""

# -------------------------
# Imports
# -------------------------

import pytest
from metrics.summary import format_summary

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
