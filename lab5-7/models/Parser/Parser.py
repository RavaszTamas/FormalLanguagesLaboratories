# LL(1)
import copy


from models.Parser.ParserOutput import ParserOutput


class Parser:

    def __init__(self, grammar):
        self.grammar = grammar
        self.firstSet = {}
        self.followSet = {}
        self.parseTable = {}
        self.constructFirst()
        self.constructFollow()
        try:
            self.generateParseTable()
        except ValueError as er:
            print(er)
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
                            concatResult = self.generateConcatenationOfLengthOne(concatResult, productionElements[i])

                        if not concatResult.issubset(self.firstSet[nonTerminal]):
                            self.firstSet[nonTerminal] = self.firstSet[nonTerminal].union(
                                self.firstSet[productionElements[0]])
                            modified = True
        # for item in self.firstSet.items():
        #     print(item)

    def generateConcatenationOfLengthOne(self, firstSet, secondSet):
        resultSet = set()
        for itemOne in firstSet:
            for itemTwo in secondSet:

                concatItem = (itemOne, itemTwo)
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
                                        self.followSet[nonTerminal] = self.followSet[nonTerminal].union(
                                            self.followSet[lhs])
                                        modified = True
                                else:
                                    if "ɛ" in self.firstSet[temp[0]]:
                                        temporarySet = copy.deepcopy(self.firstSet[temp[0]])
                                        temporarySet.remove('ɛ')
                                        temporarySet = temporarySet.union(self.followSet[lhs])

                                        if not temporarySet.issubset(self.followSet[nonTerminal]):
                                            self.followSet[nonTerminal] = self.followSet[nonTerminal].union(
                                                temporarySet)
                                            modified = True
                                    else:
                                        if not self.firstSet[temp[0]].issubset(self.followSet[nonTerminal]):
                                            self.followSet[nonTerminal] = self.followSet[nonTerminal].union(
                                                self.firstSet[temp[0]])
                                            modified = True
                            except ValueError:
                                temp = []
        # for item in self.followSet.items():
        #     print(item)

    def generateParseTable(self):
        for production in self.grammar.getEnumerated():
            rules = production[0][1].split()
            firstSet = self.firstSet[rules[0]]
            # print(production)
            # print("first",firstSet)
            for element in firstSet:
                if element != "ɛ":
                    if (production[0][0], element) not in self.parseTable:
                        self.parseTable[(production[0][0], element)] = (production[0][1], production[1])
                    else:
                        raise ValueError("Conflict at ( " + str(production[0][0])+" , "+ str(element) + " ) " + str(self.parseTable[
                            (production[0][0], element)]) + " : " + str((production[0][1], production[1])))
                else:
                    followSetOfItem = self.followSet[production[0][0]]
                    # print("follow",followSetOfItem)
                    for followElement in followSetOfItem:
                        if (production[0][0], followElement) not in self.parseTable:
                            if followElement == "ɛ":
                                self.parseTable[(production[0][0],"$")] = (production[0][1], production[1])
                            else:
                                self.parseTable[(production[0][0],followElement)] = (production[0][1], production[1])
                        else:
                            raise ValueError("Conflict at ( " + str(production[0][0]) + " , " + str(followElement) + " ) " + str(
                                self.parseTable[(production[0][0], followElement)]) + " : " + str((production[0][1], production[1])))

        for terminal in self.grammar.getTerminals():
            if terminal == "ɛ":
                 self.parseTable[("$","$")] = ("pop",-1)
            else:
                 self.parseTable[(terminal,terminal)] = ("pop",-1)

        self.parseTable[("$","$")] = ("acc",-1)

        # for item in self.parseTable.items():
        #     print(item)

    def parseSequence(self, w):
        alfa = ["$"]
        w.reverse()
        for elem in w:
            if elem == "ɛ":
                alfa.append("$")
            else:
                alfa.append(elem)
        beta = ["$", self.grammar.getStartingSymbol()[0]]
        pi = []
        go = True
        try:
            while go:
                elem = self.parseTable[(beta[-1],alfa[-1])]
                if elem[0] == "acc":
                    go = False
                elif elem[0] == "pop":
                    alfa.pop()
                    beta.pop()
                else:
                    beta.pop()
                    elems = elem[0].split()
                    elems.reverse()
                    for item in elems:
                        if item != "ɛ":
                            beta.append(item)
                    pi.append(elem[1])
        except KeyError:
            raise KeyError("Not a valid sequence")

        output = ParserOutput(self.grammar)
        output.constructTree(pi)
        return output

