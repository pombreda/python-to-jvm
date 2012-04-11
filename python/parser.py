from python.tokenizer import (TOKEN_EQUALS,
    TOKEN_IDENTIFIER,
    TOKEN_IF_STATEMENT,
    TOKEN_NEWLINE,
    TOKEN_NUMBER,
)

class ParseResult(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class AssignmentParseResult(ParseResult):
    item_type = 'assignment'
    identifier = None
    digit = None


class IfStatementParseResult(ParseResult):
    item_type = 'if_statement'
    data = None


def parse_assignment(tokens):
    types = [a.token_type for a in tokens[:4]]
    if types == [TOKEN_IDENTIFIER, TOKEN_EQUALS, TOKEN_NUMBER, TOKEN_NEWLINE]:
        identifier = tokens[0]
        digit = tokens[2]
        result = AssignmentParseResult(identifier=identifier.data, digit=digit.data)
        return result, tokens[4:]

def parse_if_statement(tokens):
    types = [a.token_type for a in tokens[:1]]
    if types == [TOKEN_IF_STATEMENT]:
        result = IfStatementParseResult(data=tokens[0].data)
        return result, tokens[1:]


def parse_tokens(tokens):
    result = []
    while tokens:
        parse = parse_assignment(tokens)
        if not parse:
            parse = parse_if_statement(tokens)
        if not parse:
            break
        item, tokens = parse 
        result.append(item)
    print("DONE", result)
    return result
