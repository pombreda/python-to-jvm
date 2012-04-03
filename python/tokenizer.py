from string import ascii_lowercase, ascii_uppercase

TOKEN_DIGIT = 'digit'
TOKEN_EQUALS = 'equals'
TOKEN_IDENTIFIER = 'identifier'
TOKEN_NEWLINE = 'newline'
TOKEN_NUMBER = 'number'


class Token(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class NewlineToken(Token):
    def __init__(self, **kwargs):
        self.token_type = TOKEN_NEWLINE
        super(NewlineToken, self).__init__(**kwargs)


class DigitToken(Token):
    def __init__(self, **kwargs):
        self.token_type = TOKEN_DIGIT
        super(DigitToken, self).__init__(**kwargs)


class NumberToken(Token):
    def __init__(self, **kwargs):
        self.token_type = TOKEN_NUMBER
        super(NumberToken, self).__init__(**kwargs)


class LowercaseToken(Token):
    def __init__(self, **kwargs):
        self.token_type = 'lowercase'
        super(LowercaseToken, self).__init__(**kwargs)


class UppercaseToken(Token):
    def __init__(self, **kwargs):
        self.token_type = 'uppercase'
        super(UppercaseToken, self).__init__(**kwargs)


class UnderscoreToken(Token):
    def __init__(self, **kwargs):
        self.token_type = 'underscore'
        super(UnderscoreToken, self).__init__(**kwargs)


class WhitespaceToken(Token):
    def __init__(self, **kwargs):
        self.token_type = 'whitespace'
        super(WhitespaceToken, self).__init__(**kwargs)


class EqualsToken(Token):
    def __init__(self, **kwargs):
        self.token_type = TOKEN_EQUALS
        super(EqualsToken, self).__init__(**kwargs)


class IdentifierToken(Token):
    def __init__(self, **kwargs):
        self.token_type = TOKEN_IDENTIFIER
        super(IdentifierToken, self).__init__(**kwargs)


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
    return tokenize_one_char(s
        , lambda c: c == character
        , lambda c: CHAR_TOKEN_CLASSES[c]
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


def tokenize_assignment(s):
    functions = (
        lambda r: tokenize_identifier(r),
        lambda r: tokenize_character(r, character=' '),
        lambda r: tokenize_character(r, character='='),
        lambda r: tokenize_character(r, character=' '),
        lambda r: tokenize_digits(r),
    )
    tokens = []
    for f in functions:
        result = f(s)
        if not result:
            return
        token, s = result
        tokens.append(token)
    number = NumberToken(data=''.join(str(t.data) for t in tokens[4]))
    return [tokens[0], tokens[2], number]


def tokenize_line(s):
    result = tokenize_assignment(s)
    if not result:
        result = []
    return result


def tokenize_python(lines):
    cleaned_lines = [l.strip('\n') for l in lines]
    tokens = []
    for line in cleaned_lines:
        tokens.extend(tokenize_line(line))
        tokens.append(NewlineToken())
    print(tokens)
    return tokens
