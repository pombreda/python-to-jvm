from string import ascii_lowercase, ascii_uppercase


class Token(object):
    def __init__(self, **kwargs):
        self.token_type = None
        for key, value in kwargs.items():
            setattr(self, key, value)


class NewlineToken(Token):
    def __init__(self, **kwargs):
        self.token_type = 'newline'
        super(NewlineToken, self).__init__(**kwargs)


class DigitToken(Token):
    def __init__(self, **kwargs):
        self.token_type = 'digit'
        super(DigitToken, self).__init__(**kwargs)


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
        self.data = '_'
        super(UnderscoreToken, self).__init__(**kwargs)


class WhitespaceToken(Token):
    def __init__(self, **kwargs):
        self.token_type = 'whitespace'
        self.data = ' '
        super(WhitespaceToken, self).__init__(**kwargs)


class EqualsToken(Token):
    def __init__(self, **kwargs):
        self.token_type = 'equals'
        self.data = '='
        super(EqualsToken, self).__init__(**kwargs)


class IdentifierToken(Token):
    def __init__(self, **kwargs):
        self.token_type = 'identifier'
        super(IdentifierToken, self).__init__(**kwargs)


def tokenize_lowercase(s):
    try:
        lower_char = s[0]
    except IndexError:
        lower_char = None
    if lower_char and lower_char in ascii_lowercase:
        return (LowercaseToken(data=lower_char), s[1:])


def tokenize_uppercase(s):
    try:
        upper_char = s[0]
    except IndexError:
        upper_char = None
    if upper_char and upper_char in ascii_uppercase:
        return (UppercaseToken(data=upper_char), s[1:])


def tokenize_digit(s):
    try:
        digit = int(s[0])
    except (IndexError, ValueError):
        digit = None
    if digit is not None:
        return (DigitToken(data=digit), s[1:])


CHAR_TOKEN_CLASSES = {
    '_': UnderscoreToken,
    ' ': WhitespaceToken,
    '=': EqualsToken,
}


def tokenize_character(s, character):
    try:
        c = s[0]
    except IndexError:
        c = None
    if c == character:
        return (CHAR_TOKEN_CLASSES[character](), s[1:])


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
    result = tokenize_identifier(s)
    if not result:
        return
    identifier, rest = result
    result = tokenize_character(rest, character=' ')
    if not result:
        return
    whitespace, rest = result
    result = tokenize_character(rest, character='=')
    if not result:
        return
    equals, rest = result
    result = tokenize_character(rest, character=' ')
    if not result:
        return
    whitespace, rest = result
    result = tokenize_digit(rest)
    if not result:
        return
    expression, rest = result
    return [identifier, equals, expression]


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
