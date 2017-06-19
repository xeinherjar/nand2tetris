def add(file_name, line_number):
    """ Pop two values from stack, add, push result onto stack"""
    asm = """
        // add
        @SP
        M=M-1
        A=M
        D=M
        @SP
        M=M-1
        A=M
        D=M+D
        M=D
        @SP
        M=M+1
    """
    print(asm)

def sub(file_name, line_number):
    """ Pop two values from stack, sub, push result onto stack"""
    asm = """
        // sub
        @SP
        M=M-1
        A=M
        D=M
        @SP
        M=M-1
        A=M
        D=M-D
        M=D
        @SP
        M=M+1
    """
    print(asm)

def neg(file_name, line_number):
    pass

def eq(file_name, line_number):
    pass

def gt(file_name, line_number):
    pass

def lt(file_name, line_number):
    pass

def _and(file_name, line_number):
    pass

def _or(file_name, line_number):
    pass

def _not(file_name, line_number):
    pass

def pop(segment, value, file_name, line_number):
    """
    Where segment is one of:
        local, argument, this, that
        static:
            Pop to static
    """
    pointers = {
        'local'   : 'LCL',  # 1
        'argument': 'ARG',  # 2
        'this'    : 'THIS', # 3
        'that'    : 'THAT', # 4
    }
    asm = ''
    if segment == 'static':
        # SP--; @file_name.value = *SP
        asm = asm + """
        // pop static
        @SP
        M=M-1
        @SP
        A=M
        D=M
        @{file_name}.{value}
        M=D
        """.format(file_name=file_name, value=value)
        print(asm)
    elif segment == 'pointer' or segment == 'temp':
        # pointer 3 + value
        # temp 5 + value
        l = { 'temp': 5, 'pointer': 3 }
        location = int(value) + l[segment]
        asm = asm + """
        // pop {segment} {value}
        @SP
        M=M-1
        A=M
        D=M
        @{location}
        M=D
        """.format(segment=segment, value=value, location=location)
    else:
        label = pointers[segment]
        asm = asm + """
        // pop {label} {value}
        @SP
        M=M-1
        @{value}
        D=A
        @{label}
        D=M+D
        @R13
        M=D
        @SP
        A=M
        D=M
        @R13
        A=M
        M=D
        """.format(label=label, value=value)



def push(segment, value, file_name, line_number):
    """
    Where segment is one of:
        local, argument, this, that:
            Push value onto stack at *segment pointer + segment offset
        constant:
            Push directly to stack
        static:
            Push to static, [16 - 255]
    """
    asm = ''
    pointers = {
        'local'   : 'LCL',  # 1
        'argument': 'ARG',  # 2
        'this'    : 'THIS', # 3
        'that'    : 'THAT', # 4
    }
    #    'temp': None, #??

    if segment == 'constant':
        # *SP = value; SP++
        asm = asm + """
        // push constant {value}
        @{value}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """.format(value=value)
    elif segment == 'static':
        # *SP = @Filename.value
        asm = asm + """
        // push static {value}
        @{file_name}.{value}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """.format(file_name=file_name, value=value)
    elif segment == 'pointer' or segment == 'temp':
        # pointer 3 + value
        # temp 5 + value
        l = { 'temp': 5, 'pointer': 3 }
        location = int(value) + l[segment]
        asm = asm + """
        // push {segment} {value}
        @{location}
        D=M
        @SP
        M=D
        @SP
        M=M+1
        """.format(segment=segment, value=value, location=location)
    else:
        label = pointers[segment]
        asm = asm + """
        // push {label} {value}
        @{value}
        D=A
        @{label}
        A=M+D
        D=M
        @SP
        M=D
        @SP
        M=M+1
        """.format(label=label, value=value)

    print(asm)

commands = {
    'add': add,
    'sub': sub,
    'neg': neg,
    'eq' : eq,
    'gt' : gt,
    'lt' : lt,
    'and': _and,
    'or' : _or,
    'not': _not,
    'pop': pop,
    'push': push,
}


def writer(command, parts, file_name, line_number):
    #print(file_name, line_number)
    commands[command](*parts, file_name=file_name, line_number=line_number)
