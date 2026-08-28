#!/usr/bin/env bash

PRG="./seq.py"
DIR="./test/input"
INPUT1="${DIR}/1.fa"
INPUT2="${DIR}/2.fa"
EMPTY="${DIR}/empty.fa"

STYLES="plain simple grid pipe orgtbl rst mediawiki latex latex_raw latex_booktabs"

for FILE in $INPUT1 $INPUT2; do
    for STYLE in $STYLES; do
        $PRG -t $STYLE $FILE > $FILE.${STYLE}.out
    done
done
echo Done.