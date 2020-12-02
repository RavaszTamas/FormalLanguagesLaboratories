from models.FA.FiniteAutomata import FiniteAutomata
from models.Grammar.Grammar import Grammar
from models.Parser.Parser import Parser
from models.Scanner.Scanner import Scanner
from models.Scanner.token import all_items, codification
from models.Scanner.ProgramInternalForm import ProgramInternalForm
from models.symbol_table.SymbolTableHashTable import SymbolTableHashTable


def scanTheFile(file_name_to_read=None):
    constant_symbol_table = SymbolTableHashTable()
    identifier_symbol_table = SymbolTableHashTable()

    pif = ProgramInternalForm()

    line_index = 1

    scanner = Scanner()

    automata_for_identifiers = FiniteAutomata()
    automata_for_integers = FiniteAutomata()
    automata_for_identifiers.parseFromFile("FA_Identifier.in")
    automata_for_integers.parseFromFile("FA_Integer.in")

    if file_name_to_read is None:
        file_name_to_read = input('enter the name of the file in the program folder:')

    with open(file_name_to_read, 'r') as file:
        for line in file:
            tokens = [token for token in scanner.token_generator(line, line_index)]
            print(tokens)
            for token in tokens:
                if token in all_items:
                    pif.add(token, -1)
                elif automata_for_identifiers.match(token):
                    id = identifier_symbol_table.pos(token)
                    pif.add(codification['identifier'], id)
                elif automata_for_integers.match(token):
                    id = constant_symbol_table.pos(token)
                    pif.add(codification['constant'], id)
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
                file.write("(" + str(item[0]) + "," + str(item[1]) + ")" + "\n")


def print_menu():
    print("""\n\n1. Full details of the Automata
2. Set of States
3. Alphabet
4. Transitions
5. Initial state
6. Final States
7. Verify sequence from standard input
0. Exit\n\n""")


def read_the_automata():
    finite_automata = FiniteAutomata()
    file_name = input("Enter the name of the file containing the automata:")
    finite_automata.parseFromFile(file_name)
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
            print("DELTA = \n" + ' \n'.join(
                [finite_automata.to_string_transition(transition) for transition in finite_automata.Delta]) + "\n")
        elif user_input == "5":
            print("q0 = " + str(finite_automata.q0) + "\n")
        elif user_input == "6":
            print("F = " + ' | '.join(finite_automata.F) + "\n")
        elif user_input == "7":
            user_input = input("Enter the token:").strip()
            if finite_automata.match(user_input):
                print("Matches")
            else:
                print("Doesn't match")
        elif user_input == "0":
            return


def print_grammar_menu():
    print("""\n\n1. Set of Terminals
2. Set of Non-terminals
3. Productions
4. Production for a non-terminal
5. Starting symbol
6. Parse from file
0. Exit\n\n""")


def readTheGrammar():

    file_name = input("Enter the name of the file containing the grammar:")
    grammar = Grammar.fromFile(file_name)
    while True:
        print_grammar_menu()
        user_input = input("Enter the command:").strip()
        if user_input == "1":
            print(grammar.E)
        elif user_input == "2":
            print(grammar.N)
        elif user_input == "3":
            print(grammar.P)
        elif user_input == "4":
            inputNonterminal = input("Enter the non-terminal:")
            print(grammar.getProductsForNonTerminal(inputNonterminal))
        elif user_input == "5":
            print(grammar.getStartingSymbol()[0])
        elif user_input == "5":
            filname = input("Enter the name of the file:")


def main():

    while True:
        print(
            "Enter 1 to parse any automata\nEnter 2 to perform scanning using the pre-existing automatas\nEnter 3 to preform a reading of a grammar\nEnter 0 to "
            "exit")
        user_input = input(">>>").strip()
        if user_input == "1":
            read_the_automata()
        elif user_input == "2":
            scanTheFile()
        elif user_input == "3":
            readTheGrammar()
        elif user_input == "0":
            return


if __name__ == '__main__':
    grammar = Grammar.fromFile("g1.txt")
    parser = Parser(grammar)
    parser.parseSequence(["a","*","(","a","+","a",")"])
    # main()
