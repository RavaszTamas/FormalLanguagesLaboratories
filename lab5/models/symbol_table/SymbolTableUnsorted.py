from models.symbol_table.SymbolTable import SymbolTable


class SymbolTableUnsorted(SymbolTable):

    def __init__(self):
        self.__table = []

    def pos(self, token):
        """
        Returns the position of the token if the token is present return it's position in the table
        otherwise insert it and return the position
        :param token: integer or string the token to be inserted or queried
        :return: int - the position inside the symbol table
        """
        if token in self.__table:
            return self.__table.index(token) + 1

        self.__table.append(token)

        return len(self.__table)
