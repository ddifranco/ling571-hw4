#!/bin/bash

PCFG='./out/hw4_trained.pcfg'
TESTS='/opt/dropbox/16-17/571/hw4/data/sentences.txt'
TOOLS='/opt/dropbox/16-17/571/hw4/tools'
GOLD='/opt/dropbox/16-17/571/hw4/data/parses.gold'

for MAXKEEP in 1 2 3 4 5 6 7 8 9 10 11 12 

do
	
	echo "N=$MAXKEEP"
	time python3 ./src/PCYK.py $PCFG $TESTS $MAXKEEP > ./experiment/exp$MAXKEEP 

	$TOOLS/evalb -p $TOOLS/COLLINS.prm $GOLD ./experiment/exp$MAXKEEP  > ./experiment/eval$MAXKEEP  
done

echo "Baseline"
time python3 ./src/PCYK.py $PCFG $TESTS > ./experiment/expBL

$TOOLS/evalb -p $TOOLS/COLLINS.prm $GOLD ./experiment/expBL  > ./experiment/evalBL

echo "999"

time python3 ./src/PCYK.py $PCFG $TESTS 999 > ./experiment/exp999 

$TOOLS/evalb -p $TOOLS/COLLINS.prm $GOLD ./experiment/exp999  > ./experiment/eval999  
