# &amp; $lt; &gt; &quot;
from enum import Enum
class State(Enum):
    PS_CLASS = 1
    PS_CLASS_VAR_DEC = 2
    PS_TYPE = 3
    PS_SUBROUTINE_DEC = 4
    PS_PARAMETER_LIST = 5
    PS_SUBROUTINE_BODY = 6
    PS_VAR_DEC = 7
    PS_CLASS_NAME = 8
    PS_SUBROUTINE_NAME = 9
    PS_VAR_NAME = 10
    S_STATEMENTS = 11
    S_STATEMENT = 12
    S_LET = 13
    S_IF = 14
    S_WHILE = 15
    S_DO = 16
    S_RETURN = 17
    E_EXPRESSION = 18
    E_TERM = 19
    E_SUBROUTINE_CALL = 20
    E_EXPRESSION_LIST = 21
    E_OP = 22
    E_UNARY_OP = 23
    E_KEYWORD_CONSTANT = 24


class Parser(object):
    AST = []
    stack = []
    current_token = None
    previous_token = None
    tokens = []
    state = State.PS_CLASS

    def next_token(self):
        for t in self.tokens:
            self.previous_token = self.current_token
            self.current_token = t
            yield t



    def add(self, token):
        tag = token['type']
        value = token['value']
        self.AST.append('<' + tag + '>')
        self.AST.append(value)
        self.AST.append('<\\' + tag + '>')

    def push(self, tag):
        self.AST.append('<' + tag + '>')
        self.stack.append(tag)

    def pop(self):
        tag = self.stack.pop()
        self.AST.append('<\\' + tag + '>')

    def ps_var_name(self, token):
        if token['type'] != 'identifier':
            print('Got ', token, ' expected an identifier')
            return
        self.add(token)


    def ps_class_name(self, token):
        if token['type'] != 'identifier':
            print('Got ', token, ' expected an identifier')
            return
        self.add(token)


    def ps_type(self, token):
        if token['type'] == 'identifier':
            self.ps_class_name(token)
        elif token['value'] in ['int', 'char', 'boolean', 'void']:
            self.add(token)
        else:
            print('Got ', token, ' expected an type of boolean, int, char or Class identifier')
            return


    def ps_class_var_dec(self, token):
        self.push('classVarDec')
        self.add(token)
        token = next(self.tokens)
        self.ps_type(token)
        token = next(self.tokens)
        self.ps_var_name(token)
        # more than one field dec on the line?
        token = next(self.tokens)
        # Can have many names declared
        while token['value'] == ',':
            self.add(token)
            token = next(self.tokens)
            self.ps_var_name(token)
            token = next(self.tokens)
        # Have we reached to the end of the field declarations?
        if token['value'] != ';':
            print('Got ', token, ' expected ;')
            return

        self.add(token)
        self.pop()


    def ps_parameter_list(self, token):
        self.push('parameterList')

        while token['value'] != ')':
            if token['value'] == ',':
                self.add(token)
                #self.ps_type(token)
                token = next(self.tokens)

            self.ps_type(token)
            token = next(self.tokens)
            if token['type'] != 'identifier':
                print('Got ', token, ' expected identifier')
                return

            self.add(token)
            token = next(self.tokens)

        if token['value'] != ')':
            print('Got ', token, ' expected (')
            return

        self.pop()
        self.add(token)

    def ps_var_dec(self, token):
        self.push('varDec')
        self.add(token) # var keyword

        token = next(self.tokens)
        self.ps_type(token)

        token = next(self.tokens)
        while token['value'] != ';':
            if token['value'] == ',':
                self.add(token)
                token = next(self.tokens)
            if token['type'] != 'identifier':
                print('Got ', token, ' expected an identifier')
                return

            self.add(token)
            token = next(self.tokens)


        self.add(token)
        self.pop()


    def ps_subroutine_body(self, token):
        self.push('subroutineBody')
        self.add(token)
        token = next(self.tokens)
        while token['value'] == 'var':
            self.ps_var_dec(token)
            token = next(self.tokens)



    def ps_subroutine_dec(self, token):
        self.push('subroutineDec')
        self.add(token)
        token = next(self.tokens)
        self.ps_type(token)

        token = next(self.tokens)
        # subroutineName
        if token['type'] != 'identifier':
            print('Got ', token, ' expected an identifier')

        self.add(token)
        token = next(self.tokens)

        # Parameter List
        if token['value'] == '(':
            self.add(token)
            token = next(self.tokens)
            self.ps_parameter_list(token)

        #body
        token = next(self.tokens)
        if token['value'] == '{':
            self.ps_subroutine_body(token)

        print('ps-subroutine-dec -- not implemented completely')
        return

    def ps_class(self, token):
        if token['value'] != 'class':
            print('Got ', token, ' expected class')
            return

        self.push('class')
        self.add(token)

        token = next(self.tokens)
        if token['type'] != 'identifier':
            print('Got ', token, ' expected an identifier')
            return

        self.add(token)
        token = next(self.tokens)
        if token['value'] != '{':
            print('Got ', token, ' expected an {')
            return

        self.add(token)

        token = next(self.tokens)
        # could have any number of each...
        while token['value'] in ['static', 'field']:
            self.ps_class_var_dec(token)
            token = next(self.tokens)

        while token['value'] in ['constructor', 'function', 'method']:
            self.ps_subroutine_dec(token)
            return


        # print('Got ', token, ' expected (class var | subroutine) declaration')




        self.pop()


    def process_tokens(self, tokens):
        self.tokens = (t for t in tokens)
        token = next(self.tokens)
        self.ps_class(token)
        print('\n'.join(self.AST))

