from models.symbol_table.SymbolTable import SymbolTable


class Node:
    """
    A structure representing a node inside our binary search tree
    the value is the token,
    the code is the position in the symbol table
    right and left are possible child nodes
    """
    def __init__(self, value, code):
        self.value = value
        self.code = code
        self.right = None
        self.left = None


class SymbolTableBinarySearchTree(SymbolTable):

    def __init__(self):
        self.__root = None
        self.__size = 0

    def pos(self, token):
        """
        Returns the position of the token if the token is present return it's position in the table
        otherwise insert it and return the position
        The table is stored using a binary search tree
        :param token: integer or string the token to be inserted or queried
        :return: int - the position inside the symbol table
        """
        current = self.__root
        parent = None

        while current is not None and current.value != token:
            parent = current
            if token < current.value:
                current = current.right
            else:
                current = current.left

        if current is None and parent is None:
            self.__size += 1
            self.__root = Node(token, self.__size)
            return self.__size
        elif current is None:
            self.__size += 1
            if token < parent.value:
                parent.right = Node(token, self.__size)
            else:
                parent.left = Node(token, self.__size)
            return self.__size
        else:
            return current.code
