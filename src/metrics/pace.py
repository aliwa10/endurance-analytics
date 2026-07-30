"""
pace.py

Pace/speed calculations for running, cycling, and swimming, built on top of
the unit conversion helpers in convert.py.

Author: Aidan Liwanag
Created: 2026-07-30
"""

from metrics.convert import meters_to_miles, meters_to_yards, mps_to_mph

def running_pace(distance, elapsed_time):
    """
    Computes running pace.

    Parameters
    ----------
    distance : float
        Distance covered, in meters.
    elapsed_time : float
        Elapsed time, in seconds.

    Returns
    -------
    float
        Pace in minutes per mile.
    """

    minutes = elapsed_time / 60
    return minutes / meters_to_miles(distance)

def cycling_speed(distance, elapsed_time):
    """
    Computes cycling speed.

    Parameters
    ----------
    distance : float
        Distance covered, in meters.
    elapsed_time : float
        Elapsed time, in seconds.

    Returns
    -------
    float
        Speed in miles per hour.
    """

    mps = distance / elapsed_time
    return mps_to_mph(mps)

def swim_pace(distance, elapsed_time):
    """
    Computes swim pace.

    Parameters
    ----------
    distance : float
        Distance covered, in meters.
    elapsed_time : float
        Elapsed time, in seconds.

    Returns
    -------
    float
        Pace per 100 yards.
    """

    yards = meters_to_yards(distance)
    minutes = elapsed_time / 60
    return minutes / (yards / 100)
