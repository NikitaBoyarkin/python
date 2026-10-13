#!/usr/bin/env bash
# Exact profiling command for the `python` EDA report (reproducible).
# Raw output: reports/eda/scripts/_profile_raw.md
set -euo pipefail

EDA="/Users/nikitaboarkin/Desktop/00 ide/00 portfolio/.eda-tools/.venv/bin/python"
PROF="/Users/nikitaboarkin/Desktop/00 obsidian/obsidian/.claude/skills/eda/scripts/eda_profile.py"
PROJECT="/Users/nikitaboarkin/Desktop/00 ide/00 portfolio/python"

cd "$PROJECT"

"$EDA" "$PROF" \
  --input data/synthetic.csv \
  --metric spend \
  --out reports/eda/scripts/_profile_raw.md

echo "--- analysis (reproduces README/segmentation numbers) ---"
"$EDA" reports/eda/scripts/analysis.py > reports/eda/scripts/_analysis_stdout.txt
echo "wrote reports/eda/scripts/_analysis_stdout.txt"

echo "--- figures ---"
"$EDA" reports/eda/scripts/plot_figures.py
