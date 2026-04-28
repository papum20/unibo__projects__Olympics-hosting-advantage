#!/bin/bash

if [ -d "src/paper/" ]; then
	cd src/paper/
fi

pdflatex main.tex
bibtex main
pdflatex main.tex