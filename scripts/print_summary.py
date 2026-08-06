"""
print_summary.py

Loads a FIT file and prints its summary to terminal.

Author: Aidan Liwanag
Created: 2026-08-06
"""

import sys
from ingestion.load_fit import load_session_fit
from metrics.summary import build_session_summary

if len(sys.argv) < 2:
    print("Usage: python scripts/print_summary.py <path/to/fit/file>")
    sys.exit(1)

filepath = sys.argv[1]
data = load_session_fit(filepath)
summary = build_session_summary(data)

# Print each key and value in the summary
for key, value in summary.items():
    print(f"{key}: {value}")
