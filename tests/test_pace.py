"""
Test suite for pace calculation functions in pace.py
"""

# -------------------------
# Imports
# -------------------------

import pytest
from metrics.pace import running_pace, cycling_speed, swim_pace

# -------------------------
# Test cases
# -------------------------

def test_running_pace_normal():
    # 1 mile in 10 minutes = 10.0 min/mile
    pace_slow = running_pace(distance=1609.344, elapsed_time=600)
    # 2 miles in 10 minutes = 5.0 min/mile
    pace_fast = running_pace(distance=3218.688, elapsed_time=600)
    assert pace_slow == pytest.approx(10.0)
    assert pace_fast == pytest.approx(5.0)

def test_running_pace_zero():
    pace1 = running_pace(distance=0, elapsed_time=600)
    pace2 = running_pace(distance=1609.344, elapsed_time=0)
    pace3 = running_pace(distance=-1609.344, elapsed_time=600)
    pace4 = running_pace(distance=1609.344, elapsed_time=-600)
    assert pace1 is None
    assert pace2 is None
    assert pace3 is None
    assert pace4 is None

def test_cycling_speed_normal():
    # 10 miles in 60 minutes = 10.0 mph
    speed_slow = cycling_speed(distance=16093.44, elapsed_time=3600)
    # 25 miles in 60 minutes = 25.0 mph
    speed_fast = cycling_speed(distance=40233.6, elapsed_time=3600)
    assert speed_slow == pytest.approx(10.0)
    assert speed_fast == pytest.approx(25.0)

def test_cycling_speed_zero():
    speed1 = cycling_speed(distance=0, elapsed_time=600)
    speed2 = cycling_speed(distance=16093.44, elapsed_time=0)
    speed3 = cycling_speed(distance=-16093.44, elapsed_time=600)
    speed4 = cycling_speed(distance=16093.44, elapsed_time=-600)
    assert speed1 is None
    assert speed2 is None
    assert speed3 is None
    assert speed4 is None

def test_swim_pace_normal():
    # 100 meters in 2 minutes = 1.8288 min/100yd (~1:49.7)
    pace_slow = swim_pace(distance=100, elapsed_time=120)
    # 400 meters in 5 minutes = 1.1430 min/100yd (~1:08.6)
    pace_fast = swim_pace(distance=400, elapsed_time=300)
    assert pace_slow == pytest.approx(1.8288, abs=1e-4)
    assert pace_fast == pytest.approx(1.1430, abs=1e-4)

def test_swim_pace_zero():
    pace1 = swim_pace(distance=0, elapsed_time=600)
    pace2 = swim_pace(distance=100, elapsed_time=0)
    pace3 = swim_pace(distance=-100, elapsed_time=600)
    pace4 = swim_pace(distance=100, elapsed_time=-600)
    assert pace1 is None
    assert pace2 is None
    assert pace3 is None
    assert pace4 is None
