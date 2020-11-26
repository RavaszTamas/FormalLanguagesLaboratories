import codecs


class Grammar:

    @staticmethod
    def processTheLine(line):
        return [value.strip().strip('"') for value in line.strip().split("=",1)[1].strip().split("|")]

    @staticmethod
    def processTheLineRule(line):
        return [value.strip().strip('"') for value in line.strip().split("=",1)[1].strip().split("\n")]

    @staticmethod
    def processRules(linesOfRules):
        result = {}
        for rule in linesOfRules:
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            rhs = [value.strip() for value in rhs.split('|')]
            for value in rhs:
                if lhs not in result:
                    result[lhs] = []
                result[lhs].append(value)
        return result


    @staticmethod
    def fromFile(fileName):
        with codecs.open(fileName,'r',encoding='utf8') as file:
            N = Grammar.processTheLine(file.readline())
            E = Grammar.processTheLine(file.readline())
            S = Grammar.processTheLine(file.readline())
            P = Grammar.processRules(Grammar.processTheLineRule(''.join([line for line in file])))
            return Grammar(N,E,P,S)



    def __init__(self,N,E,P,S):
        self.N = N
        self.E = E
        self.P = P
        self.S = S

    def getNonTerminals(self):
        return self.N

    def getTerminals(self):
        return self.E

    def getProductions(self):
        return self.P

    def getStartingSymbol(self):
        return self.S

    def getProductsForNonTerminal(self,theNonTerminal):
        return self.P[theNonTerminal]
