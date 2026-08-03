"""
Test suite for metric to imperial conversions in convert.py
"""

# -------------------------
# Imports
# -------------------------

import pytest
from metrics.convert import meters_to_miles, meters_to_yards, mps_to_mph

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
