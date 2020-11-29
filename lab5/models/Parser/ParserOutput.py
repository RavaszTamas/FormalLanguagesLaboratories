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
        return "Node " + self.id + ": " + self.value + " Father:" + str(None) if self.father is None else str(
            self.father.id) + " Sibling:" + str(None) if self.sibling is None else str(self.sibling.id)


class ParserOutput:

    def __init__(self, grammar):
        self.__grammar = grammar
        self.__nodes = []

    def constructTree(self, productions):
        count = 0
        while len(productions) != 0:
            prod = self.__grammar.getEnumerated()[productions[-1]]
            father = NodeParser(count + 1, prod[0][0], None, None)
            count += 1
            sibling = None
            rules = prod[0][1].split()
            for rule in rules:
                child = self.doesTheChildExist(rule)
                if child == None:
                    child = NodeParser(count + 1, rule, sibling, father)
                    self.__nodes.append(child)
                    sibling = child
                    count += 1
                else:
                    child.father = father
            self.__nodes.append(father)

    def doesTheChildExist(self, rule):
        for node in self.__nodes:
            if node.value == rule and node.father == None:
                return node
        return None

    def __str__(self):
        strToReturn = ""
        for node in self.__nodes:
            strToReturn += str(node) + "\n"
        return strToReturn
