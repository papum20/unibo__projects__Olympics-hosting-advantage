#!/bin/bash

if [ -d "src/paper" ]; then
	cd src/paper/
fi

texcount -inc main.tex