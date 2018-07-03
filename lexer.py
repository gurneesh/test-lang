import re
from collections import namedtuple
class TokenDef:
    def __init__(self, name, pattern, value_filter):
        self.name = name
        self.pattern = pattern
        self.value_filter = value_filter

    def __repr__(self):
        return 'TokenType.' + self.name


"""class TokenType:
    def plus(self):
        self.name = 'plus'
        self.pattern = '+'
        self.value_filter = None

    def minus(self):
        self.name = 'minus'
        self.pattern = '-'
        self.value_filter = None

    def asterisk(self):
        self.name = 'asterisk'
        self.pattern = '*'
        self.value_filter = None

    def slash(self):
        self.name = 'slash'
        self.pattern = '/'
        self.value_filter = None

    # more punctuation
    def left_paren(self):
        self.name = 'left-paren'
        self.pattern = '('
        self.value_filter = None

    def right_paren(self):
        self.name = 'right_paren'
        self.pattern = '+'
        self.value_filter = None

    #more tokens
    def integer(self):
        self.name = 'integer'
        self.pattern = re.compile('[0-9]+')
        self.value_filter = 'int'

    def whitespace(self):
        self.name = 'whitespace'
        self.pattern = re.compile('[\t]+')
        self.value_filter = None
"""
class TokenType:
    _defs = [
        #operators
        TokenDef('plus', '+', None),
        TokenDef('minus', '-', None),
        TokenDef('asterist', '*', None),
        TokenDef('slash', '/', None),

        #other punctuation
        TokenDef('left_paren', '(', None),
        TokenDef('right_paren', ')', None),

        #more tokens
        TokenDef('integer', re.compile('[0-9]+'), int),
        TokenDef('whitespace', re.compile('[\t]+'), None),
        TokenDef('print', 'print', None)
    ]

for def_ in TokenType._defs:
    setattr(TokenType, def_.name, def_)

Token = namedtuple('Token', ('type', 'value', 'slice'))


def first_token(text, start = 0):
    #print('start: ',start)
    match_text = text[start:]

    token = None
    token_text = None

    for tok in TokenType._defs:
        name = tok.name
        pattern = tok.pattern
        value_filter = tok.value_filter

        #checks
        if pattern is None:
            continue
        elif isinstance(pattern, str):
            if not match_text.startswith(pattern):
                continue
            match_value = pattern
        else:
            match = pattern.match(match_text)
            if not match:
                continue
            match_value = match.group(0)
        if token_text is not None and len(token_text)>=len(match_value):
            continue

        token_text = match_value
        #if value_filter is not None:
        #    match = value_filter(match_text)
        token = Token(tok, match_value, slice(start, start + len(token_text)))

    return token

def lex_raw(text):
    start = 0
    while True:
        if start>=len(text):
            break;
        token = first_token(text, start)
        yield token
        start = token.slice.stop


def lex_skip_whitespace(text):
    for token in lex_raw(text):
        if token.type is TokenType.whitespace:
            continue
        yield token

lex = lex_skip_whitespace

if __name__ == '__main__':
    p = list(lex('print(68+778+(8*3)/25-19)'))
    for i in p:
        print(i)

