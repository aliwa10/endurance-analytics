"""
summary.py

Builds per-session summary dicts (running, cycling, swimming) from the
DataFrames returned by load_session_fit().

Author: Aidan Liwanag
Created: 2026-08-04
"""

# -------------------------
# Imports
# -------------------------

import pandas as pd
from metrics.pace import (
    running_pace,
    cycling_speed,
    swim_pace
)
from metrics.convert import (
    meters_to_miles,
    meters_to_yards,
    mps_to_mph,
    decimal_minutes_to_mmss,
    seconds_to_hhmmss
)

# -------------------------
# Public summary functions
# -------------------------

def build_session_summary(data):
    """
    Top-level orchestrator. Detects the sport for a loaded session and
    dispatches to the matching sport-specific summary builder.

    Parameters
    ----------
    data : dict
        The dict returned by load_session_fit(), with keys "session",
        "laps", "records", "lengths", each a pandas DataFrame.

    Returns
    -------
    dict
        Session summary, as returned by the dispatched sport-specific
        builder (build_running_summary, build_cycling_summary, or
        build_swimming_summary).

    Notes
    -----
    Sport is detected from data["session"]["sport"]. The relevant
    DataFrames are extracted from `data` and passed to the appropriate
    builder based on that sport.
    """

    sport = data["session"]["sport"].values[0]
    if sport == "running":
        summary = build_running_summary(data["session"])
    elif sport == "cycling":
        summary = build_cycling_summary(data["session"])
    elif sport == "swimming":
        summary = build_swimming_summary(data["session"], data["lengths"])
    else:
        raise ValueError(f"Unrecognized sport: {sport}")

    summary["sport"] = sport

    return summary


def format_start_time(value, sport):
    """
    Extracts a human-readable start time.

    Parameters
    ----------
    value : numpy.datetime64
        The start time of an activity, to be made more human-readable.
    sport : str
        [Unused] Kept so every FORMAT_RULES entry shares the same
        (value, sport) signature.

    Returns
    -------
    string
        The start time and date, formatted as "YYYY-MM-DD HH:MM"
    """
    return pd.Timestamp(value).strftime("%Y-%m-%d %H:%M")


def format_timer_time(value, sport):
    """
    Formats timer_time for display.

    Parameters
    ----------
    value : float
        timer_time in raw seconds, as returned by the sport-specific
        summary builders.
    sport : str
        [Unused] Kept so every FORMAT_RULES entry shares the same
        (value, sport) signature.

    Returns
    -------
    string
        timer_time formatted as hh:mm:ss.
    """
    return f"{seconds_to_hhmmss(value)}"


def format_distance(value, sport):
    """
    Formats total_distance for display, in sport-appropriate units.

    Parameters
    ----------
    value : float
        total_distance already converted to miles (running/cycling) or
        yards (swimming) by the sport-specific summary builder.
    sport : str
        Sport of the session. Swimming distances are labeled "yd";
        all other sports are labeled "mi".

    Returns
    -------
    string
        Rounded distance with its unit suffix.
    """
    if sport == "swimming":
        return f"{round(value)} yd"
    else:
        return f"{round(value, 2)} mi"


def format_pace(value, sport):
    """
    Formats avg_pace for display, in sport-appropriate units.

    Parameters
    ----------
    value : float
        avg_pace in decimal minutes per mile (running) or
        per 100 yards (swimming).
    sport : str
        Sport of the session. Swimming pace is labeled "min/100yd";
        all other sports are labeled "min/mi".

    Returns
    -------
    string
        Pace formatted as mm:ss, with a per-distance unit suffix.
    """
    if sport == "swimming":
        return f"{decimal_minutes_to_mmss(value)} min/100yd"
    else:
        return f"{decimal_minutes_to_mmss(value)} min/mi"


# Maps each summary key to a (value, sport) -> str formatter. Keys not
# present here (e.g. "sport") are left unchanged by format_summary().
FORMAT_RULES = {
    "start_time": format_start_time,
    "timer_time": format_timer_time,
    "total_distance": format_distance,
    "avg_pace": format_pace,
    "avg_speed": lambda value, sport: f"{round(value, 2)} mph",
    "avg_power": lambda value, sport: f"{value} W",
    "avg_heart_rate": lambda value, sport: f"{value} bpm",
    "total_calories": lambda value, sport: f"{value} cal",
}


def format_summary(summary):
    """
    Creates a human-readable summary

    Parameters
    ----------
    summary : dict
        Session summary dict, as returned by one of the sport-specific
        builders (build_running_summary, build_cycling_summary, or
        build_swimming_summary), plus the injected "sport" key.

    Returns
    -------
    dict
        A new dict with the same keys as `summary`. Any value that was
        None is replaced with "Not Recorded"; other fields are made more
        human-readable and labeled with units; the original `summary` dict
        is not modified.

    Notes
    -----
    Formatting for each key is looked up in FORMAT_RULES. Keys without an
    entry there (e.g. "sport") are copied through unchanged.
    """

    new_summary = {}
    for key, value in summary.items(): 
        if value is None:
            new_summary[key] = "Not Recorded"
        elif key in FORMAT_RULES:
            formatter = FORMAT_RULES[key]
            new_summary[key] = formatter(value, summary["sport"])
        else:
            new_summary[key] = value

    return new_summary


def build_running_summary(session_df):
    """
    Builds a summary dict for a running session.

    Parameters
    ----------
    session_df : pandas.DataFrame
        Session-message data for the session.

    Returns
    -------
    dict
        Running session summary.

    Notes
    -----
    Fields extracted directly from Garmin's own data keep Garmin's field
    name (e.g. total_calories). Fields computed here (e.g. avg_pace, via
    running_pace() in pace.py) get names chosen for this project.
    """

    start_time = session_df["start_time"].values[0]
    timer_time = session_df["total_timer_time"].values[0]
    distance = meters_to_miles(session_df["total_distance"].values[0])
    avg_pace = running_pace(session_df["total_distance"].values[0],
                            session_df["total_timer_time"].values[0])
    avg_heart_rate = session_df["avg_heart_rate"].values[0]
    total_calories = session_df["total_calories"].values[0]

    running_summary = {
        "start_time": start_time,
        "timer_time": timer_time,
        "total_distance": distance,
        "avg_pace": avg_pace,
        "avg_heart_rate": avg_heart_rate,
        "total_calories": total_calories
    }

    return running_summary


def build_cycling_summary(session_df):
    """
    Builds a summary dict for a cycling session.

    Parameters
    ----------
    session_df : pandas.DataFrame
        Session-message data for the session.

    Returns
    -------
    dict
        Cycling session summary.

    Notes
    -----
    Fields extracted directly from Garmin's own data keep Garmin's field
    name (e.g. avg_power, total_calories). Fields computed here (e.g.
    avg_speed, via cycling_speed() in pace.py) get names chosen for this
    project. avg_power may be entirely absent from session_df (no power
    meter on the ride) and must be handled accordingly.
    """

    start_time = session_df["start_time"].values[0]
    timer_time = session_df["total_timer_time"].values[0]
    distance = meters_to_miles(session_df["total_distance"].values[0])
    avg_heart_rate = session_df["avg_heart_rate"].values[0]
    total_calories = session_df["total_calories"].values[0]
    avg_speed = cycling_speed(session_df["total_distance"].values[0],
                              session_df["total_timer_time"].values[0])
    avg_power = session_df["avg_power"].values[0]

    cycling_summary = {
        "start_time": start_time,
        "timer_time": timer_time,
        "total_distance": distance,
        "avg_speed": avg_speed,
        "avg_power": avg_power,
        "avg_heart_rate": avg_heart_rate,
        "total_calories": total_calories
    }

    return cycling_summary


def build_swimming_summary(session_df, lengths_df):
    """
    Builds a summary dict for a swimming session.

    Parameters
    ----------
    session_df : pandas.DataFrame
        Session-message data for the session.
    lengths_df : pandas.DataFrame
        Per-length data for the session.

    Returns
    -------
    dict
        Swimming session summary.

    Notes
    -----
    Fields extracted directly from Garmin's own data keep Garmin's field
    name (e.g. total_calories). Fields computed here (e.g. avg_pace, via
    swim_pace() in pace.py) get names chosen for this project.
    """

    active_swim_time = calc_active_swim_time(lengths_df)

    start_time = session_df["start_time"].values[0]
    timer_time = session_df["total_timer_time"].values[0]
    avg_heart_rate = session_df["avg_heart_rate"].values[0]
    total_calories = session_df["total_calories"].values[0]
    total_distance = meters_to_yards(session_df["total_distance"].values[0])
    avg_pace = swim_pace(session_df["total_distance"].values[0],
                         active_swim_time)

    swimming_summary = {
        "start_time": start_time,
        "timer_time": timer_time,
        "total_distance": total_distance,
        "avg_pace": avg_pace,
        "avg_heart_rate": avg_heart_rate,
        "total_calories": total_calories
    }

    return swimming_summary


def calc_active_swim_time(lengths_df):
    """
    Extracts active swim time from lengths information.

    Parameters
    ----------
    lengths_df : pandas.DataFrame
        Per-length data for the session.

    Returns
    -------
    numpy.float64
        Total active swimming time, in seconds.

    Notes
    -----
    Sums up active swim time by filtering for `active` length_type, which
    Garmin flags when the athlete is actively moving. This is specific to
    swimming because Garmin's total_timer_time does not exclude rest between
    reps the same way as it does for running and cycling.
    """
    filtered_df = lengths_df[lengths_df["length_type"] == "active"]
    total = filtered_df["total_elapsed_time"].sum()

    return total
