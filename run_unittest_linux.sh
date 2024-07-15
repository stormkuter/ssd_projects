#!/bin/bash

# Get the current directory
CURRENT_DIR=$(pwd)

# Add src, src/ssd, and tests to PYTHONPATH
export PYTHONPATH="$CURRENT_DIR/src:$CURRENT_DIR/src/ssd:$CURRENT_DIR/tests:$PYTHONPATH"

# Optional: Display the PYTHONPATH to verify
echo $PYTHONPATH

# Run pytest
pytest
