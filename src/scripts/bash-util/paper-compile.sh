#!/bin/bash

# Check for --save flag
SAVE_PDF=false
if [[ "$*" == *"--save"* ]]; then
    SAVE_PDF=true
    echo "Will save PDF to docs/paper/paper.pdf after compilation"
fi

# Find docs/paper/ absolute path before cd
DOCS_PAPER_PATH=$(find . -type d -path "*/docs/paper" 2>/dev/null | head -n 1)
if [ -n "$DOCS_PAPER_PATH" ]; then
    DOCS_PAPER_ABS=$(cd "$DOCS_PAPER_PATH" && pwd)
else
    echo "Warning: Could not find docs/paper/ directory"
    SAVE_PDF=false
    echo "Will not save PDF after compilation"
fi

# Use first argument if provided, otherwise default to src/paper1/
PAPER_DIR="${1:-src/paper1/}"

if [ -d "$PAPER_DIR" ]; then
    cd "$PAPER_DIR"
else
    echo "Error: Directory $PAPER_DIR does not exist"
    exit 1
fi

rm -f main.pdf main.aux main.bbl main.blg main.out main.log *.aux *.bbl *.blg

pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Copy to docs/paper if --save flag was set
if [ "$SAVE_PDF" = true ] && [ -f main.pdf ]; then
    cp main.pdf "$DOCS_PAPER_ABS/paper.pdf"
    echo "Saved PDF to $DOCS_PAPER_ABS/paper.pdf"
fi