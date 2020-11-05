
class FiniteAutomata:

    def __init__(self, Q=None, E=None, Delta=None, q0=None, F=None):
        self.Q = Q
        self.E = E
        self.Delta = Delta
        self.q0 = q0
        self.F = F

    def parseFromFile(self, file_name_to_read):
        with open(file_name_to_read, 'r') as file_to_read:
            self.Q = self.processTheLine(file_to_read.readline())
            self.E = self.processTheLine(file_to_read.readline())
            self.Delta = [self.processTransition(value) for value in self.processTheLine(file_to_read.readline())]
            self.q0 = self.processTheLine(file_to_read.readline())[0]
            self.F = self.processTheLine(file_to_read.readline())

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

    def to_string_transition(self ,transition):
        return "(" + str(transition[0][0]) + ", " + str(transition[0][1]) + ")" + " -> " + str(transition[1])

    def __str__(self):
        return "Q = " + ' | '.join(self.Q) + "\nE = " + ' | '.join(self.E) + "\nDELTA = \n" + ' | \n'.join \
            ([self.to_string_transition(transition) for transition in self.Delta]) +"\nq0 = " + str(
            self.q0) + "\nF = " + ' | '.join(self.F) + "\n"

    def verify_if_DFA(self):
        listOfItems = [transition[0] for transition in self.Delta]
        setOfItems = set(listOfItems)
        if len(listOfItems) == len(setOfItems):
            return True
        return False
