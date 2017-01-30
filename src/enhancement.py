#!/bin/python

import pdb

#tuple1=[(1, 3), (3, 2), (2, 1)]
#output = sorted(tuple1, key=lambda x: x[-1])
#pdb.set_trace()

def vetSubParses(nonTerminals, pointers, maxKeep, debug=False):

	bestNonTerminals = []
	bestPointers = []

	zipped  = zip(nonTerminals, pointers)
	ordered = sorted(zipped, key=lambda x: x[1][2], reverse=True)
	spotTaken = {}

	i = 0

	while i < len(nonTerminals) and len(bestNonTerminals) < maxKeep:
		nt = nonTerminals[i]
		if nt in spotTaken:			#Skip over non-terminals that are not best-in-class, even if they fare well compared to other nts
			i += 1
			continue
		spotTaken[nt] = True
		bestNonTerminals.append(ordered[i][0])
		bestPointers.append(ordered[i][1])

		i += 1

	return bestNonTerminals, bestPointers
