class ASMWriter(object):
    """Generates ASM from VM Byte Code"""
    label_counter = 0
    pointers = {
        'local'   : 'LCL',  # 1
        'argument': 'ARG',  # 2
        'this'    : 'THIS', # 3
        'that'    : 'THAT', # 4
    }

    def vm_to_asm(self, vm_op, vm_args, file_name='', line_number=''):
        """Generates ASM from VM Opcodes"""
        commands = {
            'add': self.asm_add, 'sub' : self.asm_sub, 'neg': self.asm_neg,
            'eq': self.asm_eq,   'gt': self.asm_gt,    'lt': self.asm_lt,
            'and': self.asm_and, 'or': self.asm_or,    'not': self.asm_not,
            'pop': self.asm_pop, 'push': self.asm_push
        }
        return commands[vm_op](*vm_args, file_name=file_name, line_number=line_number)

    def asm_add(self, file_name, line_number):
        """Pop two values from stack, add, push result onto stack"""
        asm = [
            "// add {file_name} {line_number}",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@SP",
            "M=M-1",
            "A=M",
            "D=D+M",
            "M=D",
            "@SP",
            "M=M+1",
        ]

        return '\n'.join(asm).format(file_name=file_name,
                                     line_number=line_number) + '\n'


    def asm_sub(self, file_name, line_number):
        """Pop two values from stack, sub, push result onto stack"""
        asm = [
            "// sub {file_name} {line_number}",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M-D",
            "M=D",
            "@SP",
            "M=M+1",
        ]

        return '\n'.join(asm).format(file_name=file_name,
                                     line_number=line_number) + '\n'


    def asm_neg(self, file_name, line_number):
        """Pop one value from stack, not, push result onto stack"""
        asm = [
            "// neg {file_name} {line_number}",
            "@SP",
            "A=M-1",
            "M=-M",
        ]

        return '\n'.join(asm).format(file_name=file_name,
                                     line_number=line_number) + '\n'

    def asm_eq(self, file_name, line_number):
        """If subtration is 0 then they are equal
        where -1 is true
               0 is false
        """
        jmp_label = str(ASMWriter.label_counter)
        ASMWriter.label_counter = ASMWriter.label_counter + 1

        asm = [
            "// eq {file_name} {line_number}",
            self.asm_sub(file_name, line_number),
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@IF_TRUE_{jmp_label}",
            "D;JEQ",
            "@IF_FALSE_{jmp_label}",
            "0;JMP",
            "(IF_TRUE_{jmp_label})",
            "  @SP",
            "  A=M",
            "  M=-1",
            "  @EQ_{jmp_label}",
            "  0;JMP",
            "(IF_FALSE_{jmp_label})",
            "  @SP",
            "  A=M",
            "  M=0",
            "  @EQ_{jmp_label}",
            "  0;JMP",
            "(EQ_{jmp_label})",
            "@SP",
            "M=M+1",
        ]
        return '\n'.join(asm).format(jmp_label=jmp_label,
                                     file_name=file_name,
                                     line_number=line_number) + '\n'


    def asm_gt(self, file_name, line_number):
        """If subtration is greater than 0 then its larger
        else its equal or smaller
        where -1 is true
               0 is false
        """
        jmp_label = str(ASMWriter.label_counter)
        ASMWriter.label_counter = ASMWriter.label_counter + 1

        asm = [
            "// gt {file_name} {line_number}",
            self.asm_sub(file_name, line_number),
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@IF_TRUE_{jmp_label}",
            "D;JGT",
            "@IF_FALSE_{jmp_label}",
            "0;JMP",
            "(IF_TRUE_{jmp_label})",
            "  @SP",
            "  A=M",
            "  M=-1",
            "  @GT_{jmp_label}",
            "  0;JMP",
            "(IF_FALSE_{jmp_label})",
            "  @SP",
            "  A=M",
            "  M=0",
            "  @GT_{jmp_label}",
            "  0;JMP",
            "(GT_{jmp_label})",
            "@SP",
            "M=M+1",
        ]

        return '\n'.join(asm).format(jmp_label=jmp_label,
                                     file_name=file_name,
                                     line_number=line_number) + '\n'


    def asm_lt(self, file_name, line_number):
        """If subtration is less than 0 then its smaller
        else its equal or larger
        where -1 is true
               0 is false
        """
        jmp_label = str(ASMWriter.label_counter)
        ASMWriter.label_counter = ASMWriter.label_counter + 1

        asm = [
            "// lt {file_name} {line_number}",
            self.asm_sub(file_name, line_number),
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@IF_TRUE_{jmp_label}",
            "D;JLT",
            "@IF_FALSE_{jmp_label}",
            "0;JMP",
            "(IF_TRUE_{jmp_label})",
            "  @SP",
            "  A=M",
            "  M=-1",
            "  @LT_{jmp_label}",
            "  0;JMP",
            "(IF_FALSE_{jmp_label})",
            "  @SP",
            "  A=M",
            "  M=0",
            "  @LT_{jmp_label}",
            "  0;JMP",
            "(LT_{jmp_label})",
            "@SP",
            "M=M+1",
        ]

        return '\n'.join(asm).format(jmp_label=jmp_label,
                                     file_name=file_name,
                                     line_number=line_number) + '\n'


    def asm_and(self, file_name, line_number):
        """Pop two values from stack, and, push result onto stack"""
        asm = [
            "// and {file_name} {line_number}",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@SP",
            "M=M-1",
            "A=M",
            "D=D&M",
            "M=D",
            "@SP",
            "M=M+1",
        ]
        return '\n'.join(asm).format(file_name=file_name,
                                     line_number=line_number) + '\n'

    def asm_or(self, file_name, line_number):
        """Pop two values from stack, or, push result onto stack"""
        asm = [
            "// or {file_name} {line_number}",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@SP",
            "M=M-1",
            "A=M",
            "D=D|M",
            "M=D",
            "@SP",
            "M=M+1",
        ]
        return '\n'.join(asm).format(file_name=file_name,
                                     line_number=line_number) + '\n'


    def asm_not(self, file_name, line_number):
        """Pop one value from stack, not, push result onto stack"""
        asm = [
            "// not {file_name} {line_number}",
            "@SP",
            "A=M-1",
            "M=!M",
        ]

        return '\n'.join(asm).format(file_name=file_name,
                                     line_number=line_number) + '\n'


    def asm_pop(self, segment, value, file_name, line_number):
        """Where segment is one of:
           local, argument, this, that, static, pointer, temp
        """
        if segment in ['static', 'pointer', 'temp']:
            if segment == 'static':
                location = "{file_name}.{value}".format(file_name=file_name, value=value)
            else:
                offset = 3 if segment == 'pointer' else 5
                location = offset + int(value)

            asm = [
                "// pop {segment} {value} {file_name} {line_number}",
                "@SP",
                "M=M-1",
                "@SP",
                "A=M",
                "D=M",
                "@{location}",
                "M=D",
            ]
        else:
            location = self.pointers[segment]
            asm = [
                "// pop {segment} {value} {file_name} {line_number}",
                "@SP",
                "M=M-1",
                "@{value}",
                "D=A",
                "@{location}",
                "D=M+D",
                "@R13",
                "M=D",
                "@SP",
                "A=M",
                "D=M",
                "@R13",
                "A=M",
                "M=D",
            ]

        return '\n'.join(asm).format(segment=segment,
                                     location=location,
                                     value=value,
                                     file_name=file_name,
                                     line_number=line_number) + '\n'

    def asm_push(self, segment, value, file_name, line_number):
        """
        Where segment is one of:
            local, argument, this, that:
                Push value onto stack at *segment pointer + segment offset
            constant:
                Push directly to stack
            static:
                Push to static, [16 - 255]
        """
        if segment in ['static', 'pointer', 'temp']:
            if segment == 'static':
                location = "{file_name}.{value}".format(file_name=file_name, value=value)
            else:
                offset = 3 if segment == 'pointer' else 5
                location = offset + int(value)

            asm = [
                "// push {segment} {value} {file_name} {line_number}",
                "@{location}",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]
        elif segment == 'constant':
            location = value
            asm = [
                "// push {segment} {value} {file_name} {line_number}",
                "@{location}",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]
        else:
            location = self.pointers[segment]
            asm = [
                "// push {segment} {value} {file_name} {line_number}",
                "@{value}",
                "D=A",
                "@{location}",
                "A=M+D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]

        return '\n'.join(asm).format(segment=segment,
                                     location=location,
                                     value=value,
                                     file_name=file_name,
                                     line_number=line_number) + '\n'



