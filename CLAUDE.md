# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Working style — please follow these rules

This is a personal learning project as well as a portfolio piece. I want to
understand every part of the codebase, not just have working code appear.

- **Explain before writing code.** For any non-trivial change, briefly explain
  your plan/approach first and wait for me to confirm before writing files.
- **Leave core logic to me.** For conceptual/logic-bearing code (test
  assertions, algorithm logic, control flow), write a stub with comments
  describing what's needed and let me fill it in — don't write it outright.
- **Library-specific syntax is fine to write directly.** Things like fitparse
  API calls, pandas boilerplate, or pytest fixture setup I haven't learned yet
  can be written directly, since these aren't the learning target.
- **Flag design decisions instead of silently making them.** If there's a
  choice with tradeoffs (e.g. naming, data structure, error handling
  approach), stop and ask me rather than picking one.
- **Keep commits small and scoped.** One logical change per commit, clear
  message. Don't bundle unrelated changes.
- **Don't touch git (commit/push) without asking first.**

# Project context

Personal triathlon training analytics tool (swim/bike/run/strength), built as
a portfolio piece for a CS degree + potential 4+1 Masters application.
Ingests Garmin FIT/CSV exports, computes real metrics, and (later) adds an
LLM layer grounded in the actual computed data.

## Commands

The package is installed editable (`pip install -e .`), which is what makes
`from ingestion.load_csv import ...`-style imports resolve in tests —
`setup.py` maps `src/` as the package root.

- Run the full test suite: `python3 -m pytest tests/`
- Run a single test file: `python3 -m pytest tests/test_load_csv.py`
- Run a single test: `python3 -m pytest tests/test_load_csv.py::test_load_valid_csv`
- Run the CSV loader directly: `python3 src/ingestion/load_csv.py data/raw/session1.csv`
- Run the FIT loader directly: `python3 src/ingestion/load_fit.py data/raw/test/test_run.fit`

## Current architecture

- `src/ingestion/load_csv.py` — CSV loader, working, has open TODOs (schema
  check, FIT-vs-CSV routing)
- `src/ingestion/load_fit.py` — FIT loader, extracts session/laps/records/
  lengths into a dict of DataFrames, calls schema validation automatically
- `src/ingestion/validate_schema.py` — `check_schema()`, validates required
  columns per sport (running/cycling/swimming) using `REQUIRED_COLUMNS`
- `tests/test_load_csv.py` — covers CSV loader (valid load, missing file,
  malformed file). This is the template/pattern to follow for FIT tests.
- No FIT tests exist yet. No metrics/analysis/visualization code exists yet
  (`src/metrics/`, `src/analysis/`, `src/visualization/`, `scripts/` are
  empty scaffolding).

## Known constraints / decisions already made

- FIT loader extracts all message types upfront into a dict (not
  sport-first-then-extract)
- Swim schema keys use plural `"lengths"` (recently renamed from `"length"`
  for consistency with `laps`/`records`)
- Multi-sport/brick-workout files are explicitly out of scope for now —
  `check_schema` assumes one sport per file
