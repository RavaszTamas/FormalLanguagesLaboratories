class FiniteAutomata:

    def __init__(self, Q=None, E=None, Delta=None, q0=None, F=None):
        self.Q = Q
        self.E = E
        self.Delta = Delta
        self.q0 = q0
        self.F = F
        self.DeltaDictionary = {}
        self.createDictionaryForTransitions()

    def parseFromFile(self, file_name_to_read):
        with open(file_name_to_read, 'r') as file_to_read:
            self.Q = self.processTheLine(file_to_read.readline())
            self.E = self.processTheLine(file_to_read.readline())
            self.Delta = [self.processTransition(value) for value in self.processTheLine(file_to_read.readline())]
            self.q0 = self.processTheLine(file_to_read.readline())[0]
            self.F = self.processTheLine(file_to_read.readline())

        if self.q0 not in self.Q:
            raise Exception("Initial state not in set of states")
        for item in self.F:
            if item not in self.Q:
                raise Exception("One of the final states is not in the FA")
        self.createDictionaryForTransitions()

    def createDictionaryForTransitions(self):
        if self.Q is None or self.E is None or self.Delta is None or self.q0 is None or self.F is None:
            return

        for state in self.Q:
            self.DeltaDictionary[state] = {}
            for transition in self.Delta:
                if transition[0][0] == state:
                    if transition[0][1] not in self.DeltaDictionary[state]:
                        self.DeltaDictionary[state][transition[0][1]] = []
                    self.DeltaDictionary[state][transition[0][1]].append(transition[1])
                    # Considering that all inputs automatas will be of type DFA this is sufficient
                    # self.DeltaDictionary[state][transition[0][1]] = transition[1]

    def processTheLine(self, line):
        return [value.strip().strip('"') for value in line.strip().split("=")[1].strip().split("|")]

    def processTransition(self, transitionString):
        src, dest = transitionString.split("->")
        src = src.strip()
        dest = dest.strip()
        params_for_transition = src[1:-1].split(",")
        src = params_for_transition[0].strip()
        value = params_for_transition[1].strip()
        return (src, value), dest

    def to_string_transition(self, transition):
        return "(" + str(transition[0][0]) + ", " + str(transition[0][1]) + ")" + " -> " + str(transition[1])

    def __str__(self):
        return "Q = " + ' | '.join(self.Q) + "\nE = " + ' | '.join(self.E) + "\nDELTA = \n" + '\n'.join \
            ([self.to_string_transition(transition) for transition in self.Delta]) + "\nq0 = " + str(
            self.q0) + "\nF = " + ' | '.join(self.F) + "\n"


    def match(self, token):
        try:
            if self.__performTransition(self.q0, token):
                return True
            return False
        except Exception:
            return False

    def __performTransition(self, state, token):
        if token == "":
            if state in self.F:
                return True
            return False

        current_character = token[0]
        if current_character not in self.E:
            raise Exception("Invalid character not in alphabet")
        try:
            for next_state in self.DeltaDictionary[state][current_character]:
                if self.__performTransition(next_state, token[1:]):
                    return True
            # next_state = self.DeltaDictionary[state][current_character]
            # return self.__performTransition(next_state,token[1:])
            #
        except KeyError as err:
            return False
