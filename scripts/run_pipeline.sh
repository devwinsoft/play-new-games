#!/bin/bash
# Wrapper script for Python pipeline
# Makes it easier to run on Linux/WSL

# Activate virtual environment if exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Run Python pipeline with all arguments
python3 scripts/run_pipeline.py "$@"

