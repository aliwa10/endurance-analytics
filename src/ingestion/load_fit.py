"""
load_fit.py

Responsible for loading a single training session FIT file and extracting
data records into a pandas DataFrame.

Author: Aidan Liwanag
Created: 2026-02-27
"""

# -------------------------
# Imports
# -------------------------

import pandas as pd
from pathlib import Path
from fitparse import FitFile
from validate_schema import check_schema

# -------------------------
# Public ingestion function
# -------------------------

def load_session_fit(filepath):
    """
    Loads a FIT file from a given path and extracts 'record', 'lap', 'session',
    and 'length' messages into pandas DataFrames and returns a dictionary of
    them.

    Parameters
    ----------
    filepath : str or Path
        Location of the FIT file.

    Returns
    -------
    data : dict
        A dictionary containing pandas DataFrames for each message type.

    Notes
    -----
    FileNotFoundError raised if path does not exist.
    """

    # Convert to Path object
    path_obj = Path(filepath)

    # Check whether the file exists
    if not path_obj.exists():
        raise FileNotFoundError(f"File not found: {path_obj}")

    # Parse the FIT file
    fitfile = FitFile(str(path_obj))

    # Create empty lists for each message type
    # you need: sessions, laps, records, lengths
    sessions = []
    laps = []
    records = []
    lengths = []

    # Loop through ALL messages in the fitfile
    # For each message, check its name
    # If it matches one of your four types, extract fields into a dict and
    # append to the right list
    for message in fitfile.get_messages():
        if message.name == "session":
            sessions.append({field.name: field.value for field in message})
        elif message.name == "lap":
            laps.append({field.name: field.value for field in message})
        elif message.name == "record":
            records.append({field.name: field.value for field in message})
        elif message.name == "length":
            lengths.append({field.name: field.value for field in message})

    # Convert each list into a DataFrame
    session_df = pd.DataFrame(sessions)
    lap_df = pd.DataFrame(laps)
    record_df = pd.DataFrame(records)
    length_df = pd.DataFrame(lengths)

    # Return a dictionary of DataFrames
    # keys should be: "session", "laps", "records", "lengths"
    data = {
        "session": session_df,
        "laps": lap_df,
        "records": record_df,
        "length": length_df
    }

    # Validate the schema of the loaded data
    check_schema(data)

    return data

# ----------------------------
# Command line execution block
# ----------------------------

if __name__ == "__main__":

    import sys

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "data/raw/test/test_run.fit"  # default test file

    data = load_session_fit(filepath)

    for key, df in data.items():
        print(f"{key}: {df.shape}")
        print(df.head())
