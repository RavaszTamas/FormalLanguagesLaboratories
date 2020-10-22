# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from models.Scanner import Scanner
from models.token import separators, all_items, codification
from models.ProgramInternalForm import ProgramInternalForm
from models.symbol_table.SymbolTableHashTable import SymbolTableHashTable

def scanTheFile():
    constant_symbol_table = SymbolTableHashTable()
    identifier_symbol_table = SymbolTableHashTable()

    pif = ProgramInternalForm()

    file_name_to_read = input('enter the name of the file in the program folder:')
    line_index = 1

    scanner = Scanner()

    with open(file_name_to_read, 'r') as file:
        for line in file:
            tokens = [token for token in scanner.token_generator(line, line_index)]
            for token in tokens:
                if token in all_items:
                    pif.add(token, -1)
                elif scanner.is_identifier(token):
                    id = identifier_symbol_table.pos(token)
                    pif.add(codification['identifier'], id)
                elif scanner.is_constant(token):
                    id = constant_symbol_table.pos(token)
                    pif.add(codification['constant'], id)
                else:
                    raise Exception('Unknown token ' + token + ' at line ' + str(line_index))
            line_index += 1


    with open("PIF.out",'w') as file:
        for item in pif.getContent():
            file.write(str(item[0]) + " -> " + str(item[1]) + "\n")

    with open("ST_constant.out",'w') as file:
        for bucket in constant_symbol_table.getContent():
            for item in bucket:
                file.write(str(item[0]) + " -> " + str(item[1]) + "\n")

    with open("ST_identifier.out",'w') as file:
        for bucket in identifier_symbol_table.getContent():
            for item in bucket:
                file.write(str(item[0]) + " -> " + str(item[1]) + "\n")

    print('\n\nCodification table: ')
    for e in codification:
        print(e, " -> ", codification[e])


if __name__ == '__main__':
    scanTheFile()
