#Parsing
"""
Parsing, syntax analysis or syntactic analysis is the process of analysing a string of symbols, either in natural language, computer languages or data structures, conforming to the rules of a formal grammar.
"""


class ParseError(Exception):
    def __init__(self, message, *tokens):
        self.message = message
        self.tokens = tokens

    def __str__(self):
        if len(self.tokens)==0:
            return self.message
        return '{0}-{1}: {2}'.format(self.tokens[0].slice.start, self.tokens[-1].slice.stop-1, self.message)

class TokenStack:
    def __init__(self, tokens):
        self._tokens = list(tokens)
        self._cursor = 0
        self._cursor_stack = []

    def peek(self):
        return self._tokens[self._cursor]
        """
        try:
            return self._tokens[self._cursor]
        except IndexError:
            raise ParseError('Unexpected end of input')
        """

    def pop(self):
        rv = self.peek()
        self._cursor += 1
        return rv

    def push_cursor(self):
        self._cursor_stack.append(self._cursor)

    def pop_cursor(self):
        self._cursor = self._cursor_stack.pop()

#Actual Parsing

class ParseBase():
    def __init__(self, token_stack):
        self.token_stack = token_stack
        self.node = self.parse()

    def parse(self):
        raise NotImplementedError()

    def pop_expecting(self, type_):
        next_token = self.token_stack.pop()
        if next_token.type is not type_:
            raise ParseError('Unexpected token: was expecting {0}, got {1}'.format(type_, next_token.type), next_token)
        return next_token

from lexer import TokenType
import ast

class IntegerLiteralExpression(ParseBase):
    def parse(self):
        int_token = self.pop_expecting(TokenType.integer)
        return ast.IntegerLiteral(int_token.value)

from lexer import lex

#print(IntegerLiteralExpression(TokenStack(lex('5'))).node)


class UnaryOpExpression(ParseBase):
    def parse(self):
        op_token = self.token_stack.pop()
        if op_token.type not in [TokenType.plus, TokenType.minus]:
            raise ParseError('Expected unary operator, got {0}'.format(op_token.type), op_token)
        rhs_node = Expression(self.token_stack).node
        return ast.UnaryOpExpression(op_token.value, rhs_node)

class BracketedExpression(ParseBase):
    def parse(self):
        self.pop_expecting(TokenType.left_paren)
        expr_node = Expression(self.token_stack).node
        self.pop_expecting(TokenType.right_paren)
        return expr_node
"""
class PrintExpression(ParseBase):
    def parse(self):
        self.pop_expecting(TokenType.print)
        self.pop_expecting(TokenType.left_paren)
        expr_node = Expression(self.token_stack, self.module, self.builder, self.printf).node
        self.pop_expecting(TokenType.right_paren)
        #print('g',expr_node)
        return ast.Print(self.modul, expr_node)
"""
class PrimaryExpression(ParseBase):
    def try_to_parse(self, parser):
        try:
            self.token_stack.push_cursor()
            return parser(self.token_stack).node, True
        except ParseError as err:
            #print(err)
            self.token_stack.pop_cursor()
            return None, False

    def parse(self):
        #print(self.token_stack.peek())
        rv, ok = self.try_to_parse(IntegerLiteralExpression)
        if ok:
            return rv
        
        rv, ok = self.try_to_parse(UnaryOpExpression)
        if ok:
            return rv

        rv, ok = self.try_to_parse(BracketedExpression)
        if ok:
            return rv
        rv, ok = self.try_to_parse(PrintExpression)
        if ok:
            #print('g',rv)
            return rv
        raise ParseError(
            'Expected integer, unary operator or bracket, Got {0}'. format(self.token_stack.peek().type), self.token_stack.peek()
        )
"""
WikiPedia's Peudocode:(copied)

parse_expression_1 (lhs, min_precedence)
    lookahead := peek next token
    while lookahead is a binary operator whose precedence is >= min_precedence
        op := lookahead
        advance to next token
        rhs := parse_primary ()
        lookahead := peek next token
        while lookahead is a binary operator whose precedence is greater
                 than op's, or a right-associative operator
                 whose precedence is equal to op's
            rhs := parse_expression_1 (rhs, lookahead's precedence)
            lookahead := peek next token
        lhs := the result of applying op with operands lhs and rhs
    return lhs

"""

class BinaryOpExpression(ParseBase):
    _op_precedence = {
        '+': 20, '-': 20,
        '*': 30, '/': 30,
    }
    def parse(self):
        primary = PrimaryExpression(self.token_stack).node
        #print(primary)
        return self.parse_expression_(primary, 0)

    def parse_expression_(self, lhs, min_precedence):
        while self.next_is_binary_() and self.precedence_() >= min_precedence:
            op_token = self.token_stack.pop()
            rhs = PrimaryExpression(self.token_stack).node
            while self.next_is_binary_() and self.precedence_()>self.precedence_(op_token):
                rhs = self.parse_expression_(rhs, self.precedence_())
            lhs = ast.BinaryOpExpression(lhs, op_token.value, rhs)
        return lhs

    def next_is_binary_(self):
        #print(self.token_stack.peek())
        try:
            next_token = self.token_stack.peek()
        except IndexError:
            return False
        return next_token.value in BinaryOpExpression._op_precedence

    def precedence_(self, token = None):
        token = token or self.token_stack.peek()
        return BinaryOpExpression._op_precedence[token.value]

Expression = BinaryOpExpression

if __name__=='__main__':
    import json
    print(json.dumps(Expression(TokenStack(lex('500+123+456*52'))).node.to_dict(), indent=2))

#print(UnaryOpExpression(TokenStack(lex('-5'))).node)
