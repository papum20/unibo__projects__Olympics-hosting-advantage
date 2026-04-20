#!/bin/bash

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

TIMESTAMP_DIR=out/scripts/regression/${TIMESTAMP}

mkdir -p $TIMESTAMP_DIR
mkdir -p $TIMESTAMP_DIR/1964/gdp/
mkdir -p $TIMESTAMP_DIR/1964/close/sep-close/
mkdir -p $TIMESTAMP_DIR/1996/gdp/
mkdir -p $TIMESTAMP_DIR/1996/close/sep-close/

find out/scripts/regression/ -maxdepth 1 -type f -name '*1964*' -exec mv {} "$TIMESTAMP_DIR/1964/" \;
find "$TIMESTAMP_DIR/1964/" -maxdepth 1 -type f -regextype posix-extended -regex '.*(\+C)[^+_].*' -exec mv {} "$TIMESTAMP_DIR/1964/close/" \;
find "$TIMESTAMP_DIR/1964/close/" -maxdepth 1 -type f -name '*sep-close1*' -exec mv {} "$TIMESTAMP_DIR/1964/close/sep-close/" \;
find "$TIMESTAMP_DIR/1964/" -maxdepth 1 -type f -name '*+G*' -exec mv {} "$TIMESTAMP_DIR/1964/gdp/" \;

find out/scripts/regression/ -maxdepth 1 -type f -name '*1996*' -exec mv {} "$TIMESTAMP_DIR/1996/" \;
find "$TIMESTAMP_DIR/1996/" -maxdepth 1 -type f -regextype posix-extended -regex '.*(\+C)[^+_].*' -exec mv {} "$TIMESTAMP_DIR/1996/close/" \;
find "$TIMESTAMP_DIR/1996/close/" -maxdepth 1 -type f -name '*sep-close1*' -exec mv {} "$TIMESTAMP_DIR/1996/close/sep-close/" \;
find "$TIMESTAMP_DIR/1996/" -maxdepth 1 -type f -name '*+G*' -exec mv {} "$TIMESTAMP_DIR/1996/gdp/" \;