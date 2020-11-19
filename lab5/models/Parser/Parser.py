
#LL(1)

class Parser:

    def __init__(self,grammar):
        self.grammar = grammar
        self.firstSet = {}
        self.followSet = {}
        self.constructFirst()

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
                        print(self.firstSet[nonTerminal])
                        print(self.firstSet[productionElements[0]])
                        if not self.firstSet[productionElements[0]].issubset(self.firstSet[nonTerminal]):
                            self.firstSet[nonTerminal] = self.firstSet[nonTerminal].union(self.firstSet[productionElements[0]])
                            modified = True

        print(self.firstSet)
    def FOLLOW(self):
        pass

