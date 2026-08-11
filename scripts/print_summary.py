"""
print_summary.py

Loads a FIT file and prints its summary to terminal.

Author: Aidan Liwanag
Created: 2026-08-06
"""

import sys
from ingestion.load_fit import load_session_fit
from metrics.summary import build_session_summary, format_summary

if len(sys.argv) < 2:
    print("Usage: python scripts/print_summary.py <path/to/fit/file>")
    sys.exit(1)

filepath = sys.argv[1]
data = load_session_fit(filepath)
summary = build_session_summary(data)
summary = format_summary(summary)

# Specify printing order
print_order = ["start_time", "sport", "total_distance", "timer_time",
               "avg_pace", "avg_speed", "avg_power", "avg_heart_rate",
               "total_calories"]

# Print each key and value in the summary
print()
for key in print_order:
    if key in summary:
        print(f"{key:<15}: {summary[key]}")
print()
