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
        enumerated = []
        index = 1
        for rule in linesOfRules:
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            rhs = [value.strip() for value in rhs.split('|')]
            for value in rhs:
                if lhs not in result:
                    result[lhs] = []
                result[lhs].append(value)
                enumerated.append(((lhs,value),index))
                index +=1
        return result,enumerated


    @staticmethod
    def fromFile(fileName):
        with codecs.open(fileName,'r',encoding='utf8') as file:
            N = Grammar.processTheLine(file.readline())
            E = Grammar.processTheLine(file.readline())
            S = Grammar.processTheLine(file.readline())
            P,enumerated = Grammar.processRules(Grammar.processTheLineRule(''.join([line for line in file])))
            return Grammar(N,E,P,S,enumerated)



    def __init__(self,N,E,P,S,enumeratedProdcutions):
        self.N = N
        self.E = E
        self.P = P
        self.S = S
        self.enumeratedProdcutions = enumeratedProdcutions

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

    def getEnumerated(self):
        return self.enumeratedProdcutions
