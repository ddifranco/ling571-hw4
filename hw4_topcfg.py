#!/bin/python3

from collections import defaultdict, Counter
from nltk import tree
from nltk import PCFG
from src.PCYK import *
import src.enhancement
import sys

if __name__ == "__main__":

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    rule_mappings = defaultdict(Counter)
    rule_totals = Counter()

    # Convert to computable form of a Parented tree and extract counts and production rules
    f = open(input_file, "r")
    rules = []
    for line in f:
        parse_tree = tree.ParentedTree.fromstring(line)
        productions = parse_tree.productions()
        for production in productions:
            rules.append(production)
            rule_mappings[production.lhs()][production.rhs()] += 1
            rule_totals[str(production.lhs())] += 1
    f.close()

    # Create PCFG from production rules and counts
    output = []
    for production in set(rules):
        lhs = production.lhs()
        rhs = production.rhs()
        prob = rule_mappings[lhs][rhs] / rule_totals[str(lhs)]
        output.append(str(production) + " [" + str(prob) + "]\n")

    # Print PCFG to file
    f = open(output_file, "w")
    f.write("".join(output))
    f.close()
