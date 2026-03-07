"""
validate_schema.py

Responsible for validating the schema of loaded FIT file data.

Author: Aidan Liwanag
Created: 2026-03-06
"""

# -------------------------
# Required columns by sport type
# -------------------------

REQUIRED_COLUMNS = {
    "running": {
        "records": ["timestamp", "distance", "heart_rate", "cadence",
                    "enhanced_altitude"],
    },
    "cycling": {
        "records": ["timestamp", "distance", "heart_rate", "cadence",
                    "enhanced_altitude", "power"],
    },
    "swimming": {
        "length": ["timestamp", "total_elapsed_time", "heart_rate"],
        "session": ["pool_length"]
    }
}

def check_schema(data):
    """
    Checks whether required schema for a given sport are present in loaded
    session data.

    Parameters
    ----------
    data : dict
        Contains pandas DataFrames with session data

    Returns
    -------
    None

    Notes
    -----
    ValueError raised if required columns are missing for the detected
    sport type.
    """

    # Detect sport type
    sport = data["session"]["sport"].values[0]

    for message_type, required_cols in REQUIRED_COLUMNS[sport].items():
        df = data[message_type]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns in {message_type} for {sport}: {missing}")

    return
