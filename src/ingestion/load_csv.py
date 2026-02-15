"""
load_csv.py

Responsible for loading a single training session CSV into a pandas DataFrame.

Author: Aidan Liwanag
Created: 2026-02-06
"""

# -------------------------
# Imports
# -------------------------

import pandas as pd
from pathlib import Path

# -------------------------
# Public ingestion function
# -------------------------

def load_session_csv(filepath):
    """
    This function loads a CSV file from a given path.

    Parameters
    ----------
    filepath : str or Path
        Povides the location of the CSV file.

    Returns
    -------
    df : DataFrame
        Holds imported CSV data.

    Notes
    -----
    FileNotFoundError raised if path does not exist.
    """

    # Convert the input filepath into a Path object
    path_obj = Path(filepath)

    # Check whether the file exists
    if not path_obj.exists():
        raise FileNotFoundError("File not found: {path_obj}")

    # Read CSV into pandas DataFrame
    df = pd.read_csv(path_obj)

    # TODO: Check schema of CSV (swim, bike, run, etc.)
    # TODO: Decide how to handle .fit files (higher resolution, ideal)

    # Return DataFrame
    return df

# ----------------------------
# Command line execution block
# ----------------------------

if __name__ == "__main__":

    # to handle command line argumets
    import sys

    if len(sys.argv) > 1:
        filepath = sys.argv[1]  # use the provided path
    else:
        filepath = "data/raw/test/test_session.csv"  # default test file
    
    # load the CSV file using the function defined above
    df = load_session_csv(filepath)

    # test by printing
    print(df.head())
