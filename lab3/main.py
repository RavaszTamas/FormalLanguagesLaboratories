# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from models.FiniteAutomata import FiniteAutomata
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
                    raise Exception('Lexical error: Unknown/Invalid token ' + token + ' at line ' + str(line_index))
            line_index += 1

    with open("PIF.out", 'w') as file:
        for item in pif.getContent():
            file.write(str(item[0]) + " -> " + str(item[1]) + "\n")

    with open("ST_constant.out", 'w') as file:
        for bucket in constant_symbol_table.getContent():
            for item in bucket:
                file.write(str(item[0]) + " -> " + str(item[1]) + "\n")

    with open("ST_identifier.out", 'w') as file:
        for bucket in identifier_symbol_table.getContent():
            for item in bucket:
                file.write(str(item[0]) + " -> " + str(item[1]) + "\n")


def print_menu():
    print("""Alma
1. Full details of the Automata
2. Set of States
3. Alphabet
4. Transitions
5. Final States
6. Verify if DFA
7. Verify sequence from standard input""")


def read_the_automata():
    finite_automata = FiniteAutomata()
    # file_name = input("Enter the name of the file containing the automata:")
    finite_automata.parseFromFile("FA.in")
    while True:
        print_menu()
        user_input = input("Enter the command:").strip()
        if user_input == "1":
            print(finite_automata)
        elif user_input == "2":
            print("Q = " + ' | '.join(finite_automata.Q) + "\n")
        elif user_input == "3":
            print("E = " + ' | '.join(finite_automata.E) + "\n")
        elif user_input == "4":
            print("DELTA = \n" + ' | \n'.join(
                [finite_automata.to_string_transition(transition) for transition in finite_automata.Delta]) + "\n")
        elif user_input == "5":
            print("F = " + ' | '.join(finite_automata.F) + "\n")
        elif user_input == "6":
            if finite_automata.verify_if_DFA():
                print("It is a DFA")
            else:
                print("It is not a DFA")
        elif user_input == "7":
            print("F = " + ' | '.join(finite_automata.F) + "\n")


if __name__ == '__main__':
    # scanTheFile()
    read_the_automata()
