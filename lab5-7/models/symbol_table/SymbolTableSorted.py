from models.symbol_table.SymbolTable import SymbolTable


class SymbolTableSorted(SymbolTable):

    def __init__(self):
        self.__table = []

    def pos(self, token):
        """
        Returns the position of the token if the token is present return it's position in the table
        otherwise insert it and return the position
        The values inside the table are sorted alphabetically by the token
        :param token: integer or string the token to be inserted or queried
        :return: int - the position inside the symbol table
        """
        for item in self.__table:
            if token == item[0]:
                return item[1]

        self.__table.append((token, len(self.__table) + 1))

        return len(self.__table)
