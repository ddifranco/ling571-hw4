#!/bin/bash

TREEBANK='/opt/dropbox/16-17/571/hw4/data/parses.train'
GOLD='/opt/dropbox/16-17/571/hw4/data/parses.gold'
TESTS='/opt/dropbox/16-17/571/hw4/data/sentences.txt'
PCFG='./out/hw4_trained.pcfg'
BASEOUT='./out/parses_base.out'
BEAMOUT='./out/parses_improved.out'
TOOLS='/opt/dropbox/16-17/571/hw4/tools'
BASERES='./out/parses_base.eval'
BEAMRES='./out/parses_improved.eval'

#PCFG Estimation
./hw4_topcfg.py $TREEBANK $PCFG

#Baseline Parses 
time ./hw4_parser.sh $PCFG $TESTS $BASEOUT

#Baseline Evaluation 
$TOOLS/evalb -p $TOOLS/COLLINS.prm $GOLD $BASEOUT > $BASERES

#Beam Parses (n may be modified within hw4_parser_improved)
time ./hw4_parser_improved.sh $PCFG $TESTS $BEAMOUT

#Beam Evaluation
$TOOLS/evalb -p $TOOLS/COLLINS.prm $GOLD $BEAMOUT > $BEAMRES
