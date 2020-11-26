
#LL(1)
import copy


class Parser:

    def __init__(self, grammar):
        self.grammar = grammar
        self.firstSet = {}
        self.followSet = {}
        self.constructFirst()
        self.constructFollow()
        self.generateParseTable()
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
                    go = True
                    for item in productionElements:
                        if len(self.firstSet[item]) == 0:
                            go = False
                            break
                    if go:
                        concatResult = copy.deepcopy(self.firstSet[productionElements[0]])
                        if 'ɛ' in concatResult:
                            concatResult.remove('ɛ')

                        for i in range(len(productionElements)):
                                concatResult = self.generateConcatenationOfLengthOne(concatResult,productionElements[i])

                        if not concatResult.issubset(self.firstSet[nonTerminal]):
                            self.firstSet[nonTerminal] = self.firstSet[nonTerminal].union(self.firstSet[productionElements[0]])
                            modified = True
        #print(self.firstSet)

    def generateConcatenationOfLengthOne(self,firstSet,secondSet):
        resultSet = set()
        for itemOne in firstSet:
            for itemTwo in secondSet:

                concatItem = (itemOne,itemTwo)
                if concatItem[0] != 'ɛ':
                    resultSet.add(concatItem[0])
                else:
                    resultSet.add(concatItem[1])
        return resultSet

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
                        temp = elements
                        while nonTerminal in temp:
                            try:
                                index = temp.index(nonTerminal)
                                temp = temp[index + 1:]
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
                                            self.followSet[nonTerminal] = self.followSet[nonTerminal].union(self.firstSet[temp[0]])
                                            modified = True
                            except ValueError:
                                temp = []
        #print(self.followSet)


    def generateParseTable(self):
        for item in self.grammar.getProductions():
            print(item)

    def parseSequence(self):
        pass