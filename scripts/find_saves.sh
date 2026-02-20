#!/bin/bash
# A simple wrapper to run the save file discovery tool

# Ensure we're in the project root or adjust path
PROJECT_ROOT=$(dirname "$(realpath "$0")")/..
cd "$PROJECT_ROOT" || exit

echo "Searching for Borderlands 4 save files..."
python scripts/main.py
