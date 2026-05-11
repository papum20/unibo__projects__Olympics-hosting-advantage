#!/bin/bash

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