#!/bin/bash
export PYTHONPATH=$(pwd)
echo $PYTHONPATH
python3 src/toPCFG.py data/parses.train out/out.pcfg data/sentences.txt > out/output2