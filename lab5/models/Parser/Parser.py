
#LL(1)
import copy


class Parser:

    def __init__(self, grammar):
        self.grammar = grammar
        self.firstSet = {}
        self.followSet = {}
        self.constructFirst()
        self.constructFollow()

    def constructFirst(self):
        for terminal in self.grammar.getTerminals():
            self.firstSet[terminal] = {terminal}

        for nonTerminal in self.grammar.getNonTerminals():
            initial = set()
            for production in self.grammar.getProductsForNonTerminal(nonTerminal):
                productionElements = production.split()
                if productionElements[0] in self.grammar.getTerminals():
                    initial.add(productionElements[0])
            self.firstSet[nonTerminal] = initial

        modified = True
        while modified:
            modified = False
            for nonTerminal in self.grammar.getNonTerminals():
                for production in self.grammar.getProductsForNonTerminal(nonTerminal):
                    productionElements = production.split()
                    if productionElements[0] in self.grammar.getNonTerminals() and productionElements[0] in self.firstSet:
                        if not self.firstSet[productionElements[0]].issubset(self.firstSet[nonTerminal]):
                            self.firstSet[nonTerminal] = self.firstSet[nonTerminal].union(self.firstSet[productionElements[0]])
                            modified = True

        print(self.firstSet)

    def constructFollow(self):
        for nonTerminal in self.grammar.getNonTerminals():
            if nonTerminal == self.grammar.getStartingSymbol()[0]:
                self.followSet[nonTerminal] = set("ɛ")
            else:
                self.followSet[nonTerminal] = set()

        modified = True
        while modified:
            modified = False
            for nonTerminal in self.grammar.getNonTerminals():
                for lhs, rhs in self.grammar.getProductions().items():
                    for production in rhs:
                        elements = production.split()
                        if nonTerminal in elements:
                            index = elements.index(nonTerminal)
                            temp = elements[index + 1:]
                            if len(temp) == 0:
                                if not self.followSet[lhs].issubset(self.followSet[nonTerminal]):
                                    self.followSet[nonTerminal] = self.followSet[nonTerminal].union(self.followSet[lhs])
                                    modified = True
                            else:
                                if "ɛ" in self.firstSet[temp[0]]:
                                    temporarySet = copy.deepcopy(self.firstSet[temp[0]])
                                    temporarySet.remove('ɛ')
                                    temporarySet = temporarySet.union(self.followSet[lhs])
                                    if not temporarySet.issubset(self.followSet[nonTerminal]):
                                        self.followSet[nonTerminal] = self.followSet[nonTerminal].union(temporarySet)
                                        modified = True
                                else:
                                    if not self.firstSet[temp[0]].issubset(self.followSet[nonTerminal]):
                                        self.followSet[nonTerminal] = self.followSet[nonTerminal].union(
                                            self.firstSet[temp[0]])
                                        modified = True
        print(self.followSet)
