class NodeParser:
    """
    A structure representing a node inside our binary search tree
    the value is the token,
    the code is the position in the symbol table
    right and left are possible child nodes
    """

    def __init__(self, id, value, sibling, father):
        self.id = id
        self.value = value
        self.sibling = sibling
        self.father = father

    def __str__(self):
        strToReturn = "Node " + str(self.id) + ": " + str(self.value) + " Father:"
        if self.father is None:
            strToReturn += " None "
        else:
            strToReturn += str(self.father.id)

        strToReturn += " Sibling: "

        if self.sibling is None:
            strToReturn += " None "
        else:
            strToReturn += str(self.sibling.id)

        return strToReturn


class ParserOutput:

    def __init__(self, grammar):
        self.__grammar = grammar
        self.__nodes = []

    def constructTree(self, productions):
        count = 0
        while len(productions) != 0:
            prod = self.__grammar.getEnumerated()[productions[0]-1]
            productions.pop(0)
            father = NodeParser(count + 1, prod[0][0], None, None)
            count += 1
            sibling = None
            rules = prod[0][1].split()
            for rule in rules:
                child = self.doesTheChildExist(rule)
                if child is None:
                    child = NodeParser(count + 1, rule, sibling, father)
                    self.__nodes.append(child)
                    sibling = child
                    count += 1
                else:
                    child.father = father
            self.__nodes.append(father)

    def doesTheChildExist(self, rule):
        for node in self.__nodes:
            if node.value == rule and node.father is None:
                return node
        return None

    def __str__(self):
        strToReturn = ""
        for node in self.__nodes:
            strToReturn += str(node) + "\n"
        return strToReturn
