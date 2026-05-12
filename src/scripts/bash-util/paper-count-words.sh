#!/bin/bash


# Use first argument if provided, otherwise default to src/paper1/
PAPER_DIR="${1:-src/paper1/}"

if [ -d "$PAPER_DIR" ]; then
    cd "$PAPER_DIR"
else
    echo "Error: Directory $PAPER_DIR does not exist"
    exit 1
fi

texcount -inc main.tex