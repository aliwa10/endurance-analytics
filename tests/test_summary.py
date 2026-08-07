"""
Test suite for session summary builders in summary.py
"""

# -------------------------
# Imports
# -------------------------

import pytest
from ingestion.load_fit import load_session_fit
from metrics.summary import (
    build_session_summary,
    build_running_summary,
    build_cycling_summary,
    build_swimming_summary,
)

# -------------------------
# Fixture paths
# -------------------------

RUNNING_FIT_PATH = "data/raw/test/test_run.fit"
CYCLING_POWER_FIT_PATH = "data/raw/test/test_bike_power.fit"
CYCLING_NOPOWER_FIT_PATH = "data/raw/test/test_bike_nopower.fit"
SWIMMING_FIT_PATH = "data/raw/test/test_pool_swim.fit"

def test_build_running_summary():
    test_dict = load_session_fit(RUNNING_FIT_PATH)
    test_summary = build_session_summary(test_dict)

    assert test_summary["timer_time"] == pytest.approx(4821.078)
    assert test_summary["total_distance"] == pytest.approx(13.205355722580132)
    assert test_summary["avg_pace"] == pytest.approx(6.084750891080165)


def test_build_cycling_summary_power():
    test_dict = load_session_fit(CYCLING_POWER_FIT_PATH)
    test_summary = build_session_summary(test_dict)

    assert test_summary["timer_time"] == pytest.approx(11257.338)
    assert test_summary["total_distance"] == pytest.approx(62.78841565258888)
    assert test_summary["avg_speed"] == pytest.approx(20.079196089893365)
    assert test_summary["avg_power"] == pytest.approx(182)


def test_build_cycling_summary_nopower():
    test_dict = load_session_fit(CYCLING_NOPOWER_FIT_PATH)
    test_summary = build_session_summary(test_dict)

    assert test_summary["timer_time"] == pytest.approx(7982.71)
    assert test_summary["total_distance"] == pytest.approx(38.34694136244333)
    assert test_summary["avg_speed"] == pytest.approx(17.293499249646548)
    assert test_summary["avg_power"] is None


def test_build_swimming_summary():
    test_dict = load_session_fit(SWIMMING_FIT_PATH)
    test_summary = build_session_summary(test_dict)

    assert test_summary["timer_time"] == pytest.approx(4057.888)
    assert test_summary["total_distance"] == pytest.approx(3425.000005206)
    assert test_summary["avg_pace"] == pytest.approx(1.5120496327381807)
