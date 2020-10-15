from math import sqrt

from models.symbol_table.SymbolTable import SymbolTable


class SymbolTableHashTable(SymbolTable):

    def __init__(self, initial_buckets=7):
        if initial_buckets <= 0:
            initial_buckets = 1
        self.__table = [[] for _ in range(initial_buckets)]
        self.__size = 0
        self.__STANDARD_LOAD_FACTOR = 0.75

    @staticmethod
    def __is_prime(the_value_to_check):
        """
        Checks if the entered integer is a prime number
        :param the_value_to_check: int - the value to be checked
        :return: True - if the value is a prime, False if it is not a prime
        """
        if the_value_to_check == 0 or the_value_to_check == 2:
            return True
        if the_value_to_check == 2:
            return True
        if the_value_to_check % 2 == 0:
            return False
        root = int(sqrt(the_value_to_check))
        i = 3
        while i <= root:
            if the_value_to_check % i == 0:
                return False
        return True

    def __next_prime(self, the_value_to_check):
        """
        Returns the next prime value after the given integer
        :param the_value_to_check: int - positive integer
        :return: int - the next prime after the entered value
        """
        the_value_to_check += 1
        while not self.__is_prime(the_value_to_check):
            the_value_to_check += 1
        return the_value_to_check

    def __hash(self, value_to_hash):
        """
        The hash function of the hash table
        :param value_to_hash: the value to be hashed
        :return: int - the hashed value for the item
        """
        return hash(value_to_hash) % (len(self.__table))

    def __rehash(self):
        """
        If the table needs to be rehashed this will perform the rehasing
        :return: None
        """
        temp_container = self.__table
        new_bucket_count = self.__next_prime(len(self.__table))

        self.__table = [[] for _ in range(new_bucket_count)]

        for item in temp_container:
            index = self.__hash(item[0])
            self.__table[index].append(item)

    def pos(self, token):
        """
        Returns the position of the token if the token is present return it's position in the table
        otherwise insert it and return the position
        The table is stored using a hash table
        :param token: integer or string the token to be inserted or queried
        :return: int - the position inside the symbol table
        """
        index = self.__hash(token)
        for item in self.__table[index]:
            if token == item[0]:
                return item[1]

        self.__size += 1
        self.__table[index].append((token, self.__size))

        load_factor = (1.0 * float(self.__size)) / float(len(self.__table))

        if load_factor > self.__STANDARD_LOAD_FACTOR:
            self.__rehash()
