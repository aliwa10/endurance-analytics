"""
Test suite for metric to imperial conversions in convert.py
"""

# -------------------------
# Imports
# -------------------------

import pytest
from metrics.convert import (
    meters_to_miles,
    meters_to_yards,
    mps_to_mph,
    decimal_minutes_to_mmss,
    seconds_to_hhmmss,
)

# -------------------------
# Test cases
# -------------------------

def test_meters_to_miles_normal():
    miles = meters_to_miles(5000)
    assert 3.11 == pytest.approx(miles, abs=1e-2)


def test_meters_to_miles_zero():
    miles = meters_to_miles(0)
    assert 0 == miles


def test_meters_to_yards_normal():
    yards = meters_to_yards(100)
    assert 109.36 == pytest.approx(yards, abs=1e-2)


def test_meters_to_yards_zero():
    yards = meters_to_yards(0)
    assert 0 == yards


def test_mps_to_mph_normal():
    mph = mps_to_mph(10)
    assert 22.37 == pytest.approx(mph, abs=1e-2)


def test_mps_to_mph_zero():
    mph = mps_to_mph(0)
    assert 0 == mph


def test_decimal_minutes_to_mmss_normal():
    mmss = decimal_minutes_to_mmss(6.0848)
    assert mmss == "6:05"


def test_decimal_minutes_to_mmss_round_up():
    mmss = decimal_minutes_to_mmss(6.996)
    assert mmss == "7:00"


def test_seconds_to_hhmmss_normal():
    hhmmss = seconds_to_hhmmss(3665)
    assert hhmmss == "1:01:05"


def test_seconds_to_hhmmss_no_hr():
    hhmmss = seconds_to_hhmmss(3010)
    assert hhmmss == "50:10"


def test_seconds_to_hhmmss_no_hr_single_min():
    mss = seconds_to_hhmmss(70)
    assert mss == "1:10"


def test_seconds_to_hhmmss_round_up_min():
    mss = seconds_to_hhmmss(59.6)
    assert mss == "1:00"


def test_seconds_to_hhmmss_round_up_hr():
    hhmmss = seconds_to_hhmmss(7199.5)
    assert hhmmss == "2:00:00"


def test_decimal_minutes_to_mmss_zero():
    mmss = decimal_minutes_to_mmss(0)
    assert mmss == "0:00"


def test_seconds_to_hhmmss_zero():
    hhmmss = seconds_to_hhmmss(0)
    assert hhmmss == "0:00"
