# All lables have to be unique...
label_counter = 0

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
        D=D+M
        M=D
        @SP
        M=M+1
    """
    return asm

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
    return asm

def neg(file_name, line_number):
    """ Pop one value from stack, not, push result onto stack"""
    asm = """
        // neg
        @SP
        A=M-1
        M=-M
    """
    return asm

def eq(file_name, line_number):
    """ If subtration is 0 then they are equal
        where -1 is true
               0 is false
    """
    global label_counter
    jmp_label = str(label_counter)
    label_counter = label_counter + 1

    sub(file_name, line_number)

    asm = """
        // eq
        @SP
        M=M-1
        A=M
        D=M
        @IF_TRUE_{label}
        D;JEQ
        @IF_FALSE_{label}
        0;JMP

        (IF_TRUE_{label})
          @SP
          A=M
          M=-1
          @EQ_{label}
          0;JMP
        (IF_FALSE_{label})
          @SP
          A=M
          M=0
          @EQ_{label}
          0;JMP

        (EQ_{label})
        @SP
        M=M+1

        """.format(label=jmp_label)
    return asm


def gt(file_name, line_number):
    """ If subtration is greater than 0 then its larger
        else its equal or smaller
        where -1 is true
               0 is false
    """
    global label_counter
    jmp_label = str(label_counter)
    label_counter = label_counter + 1

    sub(file_name, line_number)

    asm = """
        // gt
        @SP
        M=M-1
        A=M
        D=M
        @IF_TRUE_{label}
        D;JGT
        @IF_FALSE_{label}
        0;JMP

        (IF_TRUE_{label})
          @SP
          A=M
          M=-1
          @GT_{label}
          0;JMP
        (IF_FALSE_{label})
          @SP
          A=M
          M=0
          @GT_{label}
          0;JMP

        (GT_{label})
        @SP
        M=M+1

        """.format(label=jmp_label)
    return asm


def lt(file_name, line_number):
    """ If subtration is less than 0 then its smaller
        else its equal or larger
        where -1 is true
               0 is false
    """
    global label_counter
    jmp_label = str(label_counter)
    label_counter = label_counter + 1

    sub(file_name, line_number)

    asm = """
        // lt
        @SP
        M=M-1
        A=M
        D=M
        @IF_TRUE_{label}
        D;JLT
        @IF_FALSE_{label}
        0;JMP

        (IF_TRUE_{label})
          @SP
          A=M
          M=-1
          @LT_{label}
          0;JMP
        (IF_FALSE_{label})
          @SP
          A=M
          M=0
          @LT_{label}
          0;JMP

        (LT_{label})
        @SP
        M=M+1

        """.format(label=jmp_label)
    return asm


def _and(file_name, line_number):
    """ Pop two values from stack, and, push result onto stack"""
    asm = """
        // and
        @SP
        M=M-1
        A=M
        D=M
        @SP
        M=M-1
        A=M
        D=D&M
        M=D
        @SP
        M=M+1
    """
    return asm

def _or(file_name, line_number):
    """ Pop two values from stack, or, push result onto stack"""
    asm = """
        // or
        @SP
        M=M-1
        A=M
        D=M
        @SP
        M=M-1
        A=M
        D=D|M
        M=D
        @SP
        M=M+1
    """
    return asm


def _not(file_name, line_number):
    """ Pop one value from stack, not, push result onto stack"""
    asm = """
        // not
        @SP
        A=M-1
        M=!M
    """
    return asm

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
    elif segment == 'pointer' or segment == 'temp':
        # pointer 3 + value
        # temp 5 + value
        l = { 'temp': 5, 'pointer': 3 }
        location = int(value) + l[segment]
        asm = asm + """
        // pop {segment} {value}
        @SP
        M=M-1
        @SP
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

    return asm



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
        A=M
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
        A=M
        M=D
        @SP
        M=M+1
        """.format(label=label, value=value)

    return asm

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
    return commands[command](*parts, file_name=file_name, line_number=line_number)
