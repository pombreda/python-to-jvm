from python.tokenizer import (TOKEN_EQUALS,
    TOKEN_DIGIT,
    TOKEN_IDENTIFIER,
    TOKEN_NEWLINE,
)

class ParseResult(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class AssignmentParseResult(ParseResult):
    identifier = None
    digit = None


def parse_assignment(tokens):
    types = [a.token_type for a in tokens[:4]]
    if types == [TOKEN_IDENTIFIER, TOKEN_EQUALS, TOKEN_DIGIT, TOKEN_NEWLINE]:
        identifier = tokens[0]
        digit = tokens[2]
        result = AssignmentParseResult(identifier=identifier.data, digit=digit.data)
        return result, tokens[4:]

def parse_tokens(tokens):
    result = parse_assignment(tokens)
    if result:
        item, rest = result
        return [item]
    return []
