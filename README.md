# Endurance Analytics

Personal project to analyze triathlon training data and guide session-level
decisions.

## Goals
- Analyze swim, bike, run, and strength sessions to track fitness trends (e.g.
fatigue, aerobic efficiency, etc.)
- Provide logic-based guidance for training decisions without relying on
black-box metrics.

## Current Scope
- Data ingestion: load CSVs exported from Garmin
- Metrics computation: pace/HR, watts/HR, session summaries
- Analysis: session trends, fatigue detection
- Visualization: plots of metrics over time

## Setup

1. Clone the repo:
```bash
git clone https://github.com/aliwa10/endurance-analytics.git
cd endurance-analytics
```

## Folder Structure

data/raw/          # CSV session files (ignored by git)
src/ingestion/     # Scripts to load data
src/metrics/       # Scripts to compute metrics
src/analysis/      # Scripts to analyze metrics
src/visualization/ # Scripts to plot metrics
scripts/           # Orchestration scripts
tests/             # Unit tests

## Usage
- Load CSVs using the scripts in `src/ingestion/`
- Compute metrics using `src/metrics/`
- Analyze trends in `src/analysis/`
- Visualize results using `src/visualization/`

Example:
```bash
python src/ingestion/load_csv.py data/raw/session1.csv
```

## Future Work
- Compute fatigue and readiness metrics
- Integrate strength and endurance training interaction
- Generate session recommendations based on training context and readiness

## Requirements
- Python >= 3.10
- pandas, numpy, matplotlib
- Optional: seaborn, plotly, jupyter for advanced analysis