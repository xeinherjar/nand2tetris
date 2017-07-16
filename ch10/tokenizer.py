from enum import Enum
class Token(Enum):
   NEW = 0
   STR_CONSTANT = 1
   INT_CONSTANT = 2
   SYMBOL = 3
   KEYWORD_OR_IDENTIFIER = 5
   KEYWORD = 6
   IDENTIFIER = 7
   SYMBOL_OR_COMMENT = 8
   COMMENT_SL = 9
   COMMENT_ML = 10
   END = 11


class Tokenizer(object):
    previous_char = None
    current_char  = None
    token_value = ''
    state = Token.NEW
    tokens = []

    symbols = {
        '{', '}', '(', ')', '[', ']', '.', ',', ';',
        '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'
    }

    keywords = {
        'class', 'constructor', 'function', 'method', 'field', 'static',
        'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
        'this', 'let', 'do', 'if', 'else', 'while', 'return'
    }

    identifier_characters = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')

    def step(self, char):
        self.previous_char = self.current_char
        self.current_char = char
        self.state = self.transitions[self.state](self)

    def new(self):
        char = self.current_char
        self.token_value = ''
        if (char.isspace()):
            return Token.NEW
        if (char.isdigit()):
            self.token_value = self.token_value + char
            return Token.INT_CONSTANT
        if (char is '"'):
            # we dont write because we dont need to quotes
            return Token.STR_CONSTANT
        if (char in self.symbols and char != '/'):
            self.token_value = self.token_value + char
            return self.transitions[Token.SYMBOL](self)
        if (char in self.symbols and char == '/'):
            # we dont write because we dont comments
            # is either the / symbol or start of comment
            return Token.SYMBOL_OR_COMMENT
        if (char in self.identifier_characters):
            # is indentifier or keyword
            self.token_value = self.token_value + char
            return Token.KEYWORD_OR_IDENTIFIER

    def str_constant(self):
        if (self.current_char == '"'):
            return self.transitions[Token.END](self, 'STR_CONSTANT')

        self.token_value = self.token_value + self.current_char
        return Token.STR_CONSTANT

    def int_constant(self):
        if (not self.current_char.isdigit()):
            self.transitions[Token.END](self, 'INT_CONSTANT')
            return self.transitions[Token.NEW](self)

        self.token_value = self.token_value + self.current_char
        return Token.INT_CONSTANT

    def symbol(self):
        return self.transitions[Token.END](self, 'SYMBOL')

    def keyword_or_identifier(self):
        if (self.current_char.isspace()):
            if (self.token_value in self.keywords):
                return self.transitions[Token.KEYWORD](self)
            else:
                return self.transitions[Token.IDENTIFIER](self)

        if (self.current_char not in self.identifier_characters):
            if (self.token_value in self.keywords):
                self.transitions[Token.END](self, 'KEYWORD')
            else:
                self.transitions[Token.END](self, 'IDENTIFIER')
            return self.transitions[Token.NEW](self)

        self.token_value = self.token_value + self.current_char
        return Token.KEYWORD_OR_IDENTIFIER

    def keyword(self):
        return self.transitions[Token.END](self, 'KEYWORD')

    def indentifier(self):
        return self.transitions[Token.END](self, 'IDENTIFIER')

    def symbol_or_comment(self):
        if (self.current_char is '/'):
            return Token.COMMENT_SL
        if (self.current_char is '*'):
            return Token.COMMENT_ML

        self.token_value = self.token_value + self.current_char
        self.transitions[Token.SYMBOL](self)
        return self.transistion[Token.NEW](self)

    def comment_sl(self):
        if (self.current_char is '\n'):
            return Token.NEW

        return Token.COMMENT_SL

    def comment_ml(self):
        if (self.current_char is '/' and self.previous_char is '*'):
            return Token.NEW

        return Token.COMMENT_ML

    def end(self, token_type):
        token = { 'value': self.token_value, 'type': token_type }
        self.tokens.append(token)
        return Token.NEW

    def process_file(self, source_file):
        with open(source_file, 'r') as source:
            for line in source:
                for char in line:
                    self.step(char)

        return self.tokens;

    transitions = {
        Token.NEW: new,
        Token.STR_CONSTANT: str_constant,
        Token.INT_CONSTANT: int_constant,
        Token.SYMBOL: symbol,
        Token.KEYWORD_OR_IDENTIFIER: keyword_or_identifier,
        Token.KEYWORD: keyword,
        Token.IDENTIFIER: indentifier,
        Token.SYMBOL_OR_COMMENT: symbol_or_comment,
        Token.COMMENT_SL: comment_sl,
        Token.COMMENT_ML: comment_ml,
        Token.END: end,
    }
