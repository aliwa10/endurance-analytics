"""
convert.py

Unit conversion helpers used throughout the metrics layer.

Author: Aidan Liwanag
Created: 2026-07-30
"""

def meters_to_miles(meters):
    """
    Converts a distance in meters to miles.

    Parameters
    ----------
    meters : float
        Distance in meters.

    Returns
    -------
    float
        Distance in miles.
    """

    return meters / 1609.344

def meters_to_yards(meters):
    """
    Converts a distance in meters to yards.

    Parameters
    ----------
    meters : float
        Distance in meters.

    Returns
    -------
    float
        Distance in yards.
    """

    return meters * 1.0936133

def mps_to_mph(mps):
    """
    Converts a speed in meters per second to miles per hour.

    Parameters
    ----------
    mps : float
        Speed in meters per second.

    Returns
    -------
    float
        Speed in miles per hour.
    """

    return mps * 2.2369363
