from models.token import separators
import re


def is_identifier(token):
    return re.match(r'^[a-zA-Z]([a-zA-Z]|[0-9]|_){,256}$', token) is not None


def is_constant(token):
    return re.match(r'^(0|[+-]?([0-9]*[.])?[0-9]+|[\+\-]?[1-9][0-9]*)$|^\'.\'$|^\".*\"$', token) is not None


def is_escaped_quotation_mark(line, index):
    if index == 0:
        return False
    elif line[index - 1] == '\\':
        return True
    else:
        return False


def get_string(line, index):
    token = ''
    number_of_quotation_mark = 0

    while index < len(line) and number_of_quotation_mark < 2:
        if line[index] == '"' and not is_escaped_quotation_mark(line, index):
            number_of_quotation_mark += 1
        token += line[index]
        index += 1

    return token, index


def token_generator(line, line_index):
    tokens = []
    token = ''
    index = 0
    while index < len(line):
        if line[index] == '"':
            if token:
                tokens.append(token)
            token, index = get_string(line, index)
            if token[-1] != '"':
                raise Exception(
                    "Syntax error, string is not closed! at line " + line_index + " position " + index + "\n")
            tokens.append(token)
            token = ''
        elif line[index] in separators:
            if token:
                tokens.append(token)
            tokens.append(line[index])
            index += 1
            token = ''
        else:
            token += line[index]
            index += 1
    if token:
        tokens.append(token)
    return tokens
