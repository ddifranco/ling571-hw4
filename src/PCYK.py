"""
CYK Parser
@author: Will Kearns
"""
import sys
import nltk
import pandas as pd
from math import log10 as log
from operator import itemgetter
import enhancement

def iterable_df(size):
    """
    Initializes a symmetric Pandas DataFrame of lists.
    :param size: the dimension of the symmetric matrix.
    :return: Pandas DataFrame
    """
    df = pd.DataFrame(columns=range(size), index=range(size))
    return df.applymap(lambda x: [])


class Node:

    def __init__(self, _id, left, right):
        """
        A vertex of the parse tree

        :param _id: Identifier, in the case of CYK is a Non-terminal
        :param left: Child of left branch of tree w.r.t. this node
        :param right: Child of right branch of tree w.r.t. this node
        """
        self.id = _id
        self.left = left
        self.right = right

    def print(self):
        sys.stdout.write("(" + self.id + " ")


class CYK:

    def __init__(self):
        self.table = None
        self.shadow_matrix = None
        self.tokens = None

    def parse(self, sentence, grammar, maxKeep=None):
        """
        Fills the CYK table with nonterminal tags corresponding to word spans.

        :param sentence: String to be parsed by the grammar.
        :param grammar: Context-free Grammar as NLTK CFG Object.
        :return: CYK table
        """
        self.tokens = nltk.word_tokenize(sentence)
        self.table = iterable_df(len(self.tokens))
        self.shadow_matrix = iterable_df(len(self.tokens))

        for i, word in enumerate(self.tokens):
            # Initial Non-terminals are assigned based on Lexical rules
            for rule in grammar.productions():
                if rule.is_lexical() and rule.rhs()[0] == word:
                    self.table.iloc[i][i].append(str(rule.lhs()))
            # Merge
            j = i - 1
            while j >= 0:
                k = j + 1
                while k <= i:
                    non_lexical_match = []
                    pointers = []
                    for idx1, B in enumerate(self.table.iloc[j][k-1]):
                        for idx2, C in enumerate(self.table.iloc[k][i]):
                            for rule in grammar.productions():
                                logprob = 0
                                if rule.is_nonlexical() and str(rule.rhs()[0]) == B and str(rule.rhs()[1]) == C:
                                    non_lexical_match.append(str(rule.lhs()))
                                    if self.shadow_matrix.iloc[j][k-1]:
                                        logprob += self.shadow_matrix.iloc[j][k-1][idx1][2]
                                    if self.shadow_matrix.iloc[k][i]:
                                        logprob += self.shadow_matrix.iloc[k][i][idx2][2]
                                    logprob += log(rule.prob())
                                    pointers.append(((j, k-1, idx1),
                                                     (k, i, idx2), logprob))
                    for element in self.table.iloc[j][i]:
                        non_lexical_match.append(element)
                    for element in self.shadow_matrix.iloc[j][i]:
                        pointers.append(element)
                    if maxKeep is not None:
                        non_lexical_match, pointers = enhancement.vetSubParses(non_lexical_match, pointers, maxKeep)
                    self.table.iloc[j][i] = non_lexical_match
                    self.shadow_matrix.iloc[j][i] = pointers
                    k += 1
                j -= 1
        return self.table


    def spawn_nodes(self, row, column, nonterminal, index):
        """
        Creates a node and recursively generates its children.

        :param row: row of parent node in table.
        :param column: column of parent node in table.
        :param nonterminal: id of node
        :param index: index of target nonterminal
        :return:
        """
        pointers = self.shadow_matrix.iloc[row][column]
        if not pointers:
            sys.stdout.write("(" + nonterminal + " ")
            sys.stdout.write(self.tokens[column] + ")")
            return None
        else:
            sys.stdout.write("(" + nonterminal + " ")
            # Spawn left child
            B = pointers[index][0]
            _id = self.table.iloc[B[0]][B[1]][B[2]]
            left = self.spawn_nodes(B[0], B[1], _id, B[2])

            # Spawn right child
            C = pointers[index][1]
            _id = self.table.iloc[C[0]][C[1]][C[2]]
            right = self.spawn_nodes(C[0], C[1], _id, C[2])

            sys.stdout.write(")")

        return Node(nonterminal, left, right)

    def top_tree(self):
        rows, cols = self.table.shape
        i, j = 0, cols - 1
        probs = [x[2] for x in self.shadow_matrix.iloc[i][j]]
        if probs:
            index, value = max(enumerate(probs), key=itemgetter(1))
            self.spawn_nodes(i, j, self.table.iloc[i][j][index], index)
        sys.stdout.write("\n")

if __name__ == "__main__":

    maxKeep = None
    if len(sys.argv) == 4:
        maxKeep = int(sys.argv[3])

    grammar_file = open(sys.argv[1], "r")
    cfg = nltk.PCFG.fromstring(grammar_file.read())
    grammar_file.close()

    sentence_file = open(sys.argv[2], "r")
    for line in sentence_file:
        #sys.stdout.write(line)
        cyk = CYK()
        parse_table = cyk.parse(line, cfg, maxKeep)
        cyk.top_tree()
    sentence_file.close()
