#!/bin/bash

if [ -d "src/paper/" ]; then
	cd src/paper/
fi

rm -f main.aux main.bbl main.blg main.out main.log *.aux *.bbl *.blg

pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex