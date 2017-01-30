#!/bin/python3

from nltk import PCFG
from PCYK import *
import pdb

# Load PCFG and run PCYK

pcfg = PCFG.fromstring(open(sys.argv[1]))
sentence_file = open(sys.argv[2], "r")

for line in sentence_file:
	cyk = CYK()
	parse_table = cyk.parse(line, pcfg)
	#pdb.set_trace()
	#print(parse_table)
	trees = cyk.top_tree()
sentence_file.close()
