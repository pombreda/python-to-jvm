from string import ascii_lowercase, ascii_uppercase

TOKEN_CHARACTER = 'character'
TOKEN_DIGIT = 'digit'
TOKEN_EQUALS = 'equals'
TOKEN_IDENTIFIER = 'identifier'
TOKEN_IF_STATEMENT = 'if'
TOKEN_KEYWORD = 'keyword'
TOKEN_LOWERCASE = 'lowercase'
TOKEN_NEWLINE = 'newline'
TOKEN_NUMBER = 'number'
TOKEN_UNDERSCORE = 'underscore'
TOKEN_UPPERCASE = 'uppercase'
TOKEN_WHITESPACE = 'whitespace'


class Token(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class NewlineToken(Token):
    token_type = TOKEN_NEWLINE


class DigitToken(Token):
    token_type = TOKEN_DIGIT


class NumberToken(Token):
    token_type = TOKEN_NUMBER


class LowercaseToken(Token):
    token_type = TOKEN_LOWERCASE


class UppercaseToken(Token):
    token_type = TOKEN_UPPERCASE


class UnderscoreToken(Token):
    token_type = TOKEN_UNDERSCORE


class WhitespaceToken(Token):
    token_type = TOKEN_WHITESPACE


class EqualsToken(Token):
    token_type = TOKEN_EQUALS


class IdentifierToken(Token):
    token_type = TOKEN_IDENTIFIER

    
class KeywordToken(Token):
    token_type = TOKEN_KEYWORD


class IfStatementToken(Token):
    token_type = TOKEN_IF_STATEMENT


class CharacterToken(Token):
    token_type = TOKEN_CHARACTER


CHAR_TOKEN_CLASSES = {
    '_': UnderscoreToken,
    ' ': WhitespaceToken,
    '=': EqualsToken,
}


def tokenize_one_char(s, f_valid, token_class):
    try:
        c = s[0]
    except IndexError:
        c = None
    if f_valid(c):
        return (token_class(c)(data=c), s[1:])    


def tokenize_lowercase(s):
    return tokenize_one_char(s
        , lambda c: c and c in ascii_lowercase
        , lambda c: LowercaseToken
    )


def tokenize_uppercase(s):
    return tokenize_one_char(s
        , lambda c: c and c in ascii_uppercase
        , lambda c: UppercaseToken
    )


def tokenize_character(s, character):
    try:
        token_class = CHAR_TOKEN_CLASSES[character]
    except KeyError:
        token_class = CharacterToken
    return tokenize_one_char(s
        , lambda c: c == character
        , lambda c: token_class
    )


def tokenize_digit(s):
    try:
        digit = int(s[0])
    except (IndexError, ValueError):
        digit = None
    if digit is not None:
        return (DigitToken(data=digit), s[1:])


def tokenize_digits(s):
    digits = []
    rest = s
    while rest:
        result = tokenize_digit(rest)
        if not result:
            break
        d, rest = result
        digits.append(d)
    if digits:
        return digits, rest


def tokenize_letter(s):
    result = tokenize_lowercase(s)
    if not result:
        result = tokenize_uppercase(s)
    if result:
        return result


def tokenize_keyword(s, keyword):
    c_tokens = []
    rest = s
    for c in keyword:
        result = tokenize_character(rest, character=c)
        if not result:
            return
        cr, rest = result
        c_tokens.append(cr)
    return KeywordToken(data=''.join(t.data for t in c_tokens)), rest


def tokenize_identifier(s):
    result = tokenize_letter(s)
    if not result:
        result = tokenize_character(s, character='_')
    if not result:
        return
    identifier = []
    first, rest = result
    identifier.append(first)
    while rest:
        result = tokenize_letter(rest)
        if not result:
            result = tokenize_digit(rest)
        if not result:
            result = tokenize_character(rest, character='_')
        if not result:
            break
        c, rest = result
        identifier.append(c)
    identifier_str = ''.join([t.data for t in identifier])
    return (IdentifierToken(data=identifier_str), rest)


def _tokenize_functions(s, functions):
    tokens = []
    for f in functions:
        result = f(s)
        if not result:
            return
        token, s = result
        if type(token) == list:
            tokens.extend(token)
        else:
            tokens.append(token)
    return tokens

def tokenize_assignment(s):
    functions = (
        lambda r: tokenize_identifier(r),
        lambda r: tokenize_character(r, character=' '),
        lambda r: tokenize_character(r, character='='),
        lambda r: tokenize_character(r, character=' '),
        lambda r: tokenize_digits(r),
    )
    tokens = _tokenize_functions(s, functions)
    if not tokens:
        return
    digits = [t for t in tokens if t.token_type == TOKEN_DIGIT]
    number = NumberToken(data=''.join(str(t.data) for t in digits))
    return [tokens[0], tokens[2], number]


def tokenize_if_statement(s):
    functions = (
        lambda r: tokenize_keyword(r, 'if'),
        lambda r: tokenize_character(r, character=' '),
        lambda r: tokenize_identifier(r),
        lambda r: tokenize_character(r, character=' '),
        lambda r: tokenize_character(r, character='>'),
        lambda r: tokenize_character(r, character=' '),
        lambda r: tokenize_digits(r),
        lambda r: tokenize_character(r, character=':'),
    )
    tokens = _tokenize_functions(s, functions)
    if not tokens:
        return
    data = (tokens[2], tokens[4], tokens[6])
    return [IfStatementToken(data=data)] 
    

def tokenize_line(s):
    result = tokenize_assignment(s)
    if not result:
        result = tokenize_if_statement(s)
    if not result:
        result = []
    return result


def tokenize_python(lines):
    cleaned_lines = [l.strip('\n') for l in lines]
    tokens = []
    for line in cleaned_lines:
        tokens.extend(tokenize_line(line))
        tokens.append(NewlineToken())
    return tokens
