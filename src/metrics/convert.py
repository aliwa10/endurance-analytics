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


def decimal_minutes_to_mmss(decimal_minutes):
    """
    Formats a pace/speed value given in decimal minutes as a mm:ss string.

    Parameters
    ----------
    decimal_minutes : float
        A duration in decimal minutes (e.g. 6.0848).

    Returns
    -------
    str
        Formatted as "m:ss" — minutes are not zero-padded, seconds are
        always zero-padded to two digits (e.g. "6:05").
    """

    total_seconds = round(decimal_minutes * 60)
    minutes, seconds = divmod(total_seconds, 60)

    return f"{minutes}:{seconds:02d}"


def seconds_to_hhmmss(total_seconds):
    """
    Formats a duration given in seconds as an h:mm:ss or m:ss string.

    Parameters
    ----------
    total_seconds : float
        A duration in seconds (e.g. 4821.078).

    Returns
    -------
    str
        Formatted as "h:mm:ss" when the duration is one hour or longer
        (minutes and seconds zero-padded to two digits, e.g. "1:20:21").
        When the duration is under one hour, the hours portion is
        omitted and the result is formatted as "m:ss" (minutes not
        zero-padded, seconds zero-padded to two digits, e.g. "20:21").
    """

    total_seconds = round(total_seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours >= 1:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"
