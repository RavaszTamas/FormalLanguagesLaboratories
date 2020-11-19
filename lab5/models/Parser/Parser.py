
#LL(1)

class Parser:

    def __init__(self,grammar):
        self.grammar = grammar
        self.firstSet = {}
        self.followSet = {}
        self.constructFirst()

    def constructFirst(self, nonTerminal):
        for terminal in self.grammar.getTerminals():
            self.followSet[terminal] = {terminal}

    def FOLLOW(self):
        pass

