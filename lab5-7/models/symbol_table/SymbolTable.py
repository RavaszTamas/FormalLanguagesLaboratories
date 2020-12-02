class SymbolTable:
    """
    Interface for the symbol table
    """
    def pos(self, token):
        """
        Returns the position of the token inside the symbol table
        if it is not inside it will add it and returns it's position
        :param token: the token to be searched
        :return: int - the position inside the symbol table
        """
        pass
