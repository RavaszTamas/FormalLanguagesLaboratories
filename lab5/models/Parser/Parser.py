
#LL(1)

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
                self.followSet[nonTerminal] = {"$"}
            else:
                self.followSet[nonTerminal] = {}

        for nonTerminal in self.grammar.getNonTerminals():
            follow = []
            found = False
            for production in self.grammar.getProductsForNonTerminal(nonTerminal):
                #lhs = self.grammar.getProductions[production] need a first or default :(
                rhs = production.split()
                for elem in range(0,len(rhs),1):
                    if rhs[elem] == nonTerminal and found == False:
                        found = True
                    if found == True and elem + 1 < len(rhs):
                        follow.append(rhs[elem+1])
                follow.append("")
                for f in follow:
                    if f == "":
                        self.followSet[nonTerminal] = self.followSet[nonTerminal].union(
                            {"placeholder"})
                        break
                    else:
                        if f in self.grammar.getTerminals():
                            self.followSet[nonTerminal] = self.followSet[nonTerminal].union({f})
                            break
                        else:
                            if "epsilon" in self.firstSet[f]:
                                firstFCopy = self.firstSet[f]
                                firstFCopy.remove("epsilon")
                                self.followSet[nonTerminal] = self.followSet[nonTerminal].union(firstFCopy)
                                break
                            else:
                                self.followSet[nonTerminal] = self.followSet[nonTerminal].union(self.firstSet[f])
                                break

        print(self.followSet)
