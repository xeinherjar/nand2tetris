
        // push constant 3030
        @3030
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // pop pointer 0
        @SP
        M=M-1
        @SP
        A=M
        D=M
        @3
        M=D
        

        // push constant 3040
        @3040
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // pop pointer 1
        @SP
        M=M-1
        @SP
        A=M
        D=M
        @4
        M=D
        

        // push constant 32
        @32
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // pop THIS 2
        @SP
        M=M-1
        A=M
        D=M

        @2
        D=A
        @THIS
        D=M+D
        @R13
        M=D
        @SP
        A=M
        D=M
        @R13
        A=M
        M=D
        

        // push constant 46
        @46
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // pop THAT 6
        @SP
        M=M-1
        A=M
        D=M

        @6
        D=A
        @THAT
        D=M+D
        @R13
        M=D
        @SP
        A=M
        D=M
        @R13
        A=M
        M=D
        

        // push pointer 0
        @3
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // push pointer 1
        @4
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

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
    

        // push THIS 2
        @2
        D=A
        @THIS
        A=M+D
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

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
    

        // push THAT 6
        @6
        D=A
        @THAT
        A=M+D
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

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
    
