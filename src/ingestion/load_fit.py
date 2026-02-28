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

# -------------------------
# Public ingestion function
# -------------------------

def load_session_fit(filepath):
    """
    Loads a FIT file from a given path and extracts 'record' messages
    (second-by-second telemetry) into a pandas DataFrame.

    Parameters
    ----------
    filepath : str or Path
        Location of the FIT file.

    Returns
    -------
    df : DataFrame
        Each row is one telemetry record. Columns vary by device and activity.

    Notes
    -----
    FileNotFoundError raised if path does not exist.
    Raises ValueError if file contains no 'record' messages.
    """

    # Convert to Path object
    path_obj = Path(filepath)

    # Check whether the file exists
    if not path_obj.exists():
        raise FileNotFoundError(f"File not found: {path_obj}")

    # Parse the FIT file
    fitfile = FitFile(str(path_obj))

    # Extract 'record' messages (second-by-second telemetry)
    records = []
    for message in fitfile.get_messages("record"):
        records.append({field.name: field.value for field in message})

    # Check that we actually got something
    if not records:
        raise ValueError(f"No telemetry records found in: {path_obj}")

    # Convert list of dicts into a DataFrame
    df = pd.DataFrame(records)

    # TODO: schema validation (check for expected columns by sport type)

    return df

# ----------------------------
# Command line execution block
# ----------------------------

if __name__ == "__main__":

    import sys

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "data/raw/test/test_run.fit"  # default test file

    df = load_session_fit(filepath)

    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"\nColumns: {df.columns.tolist()}")