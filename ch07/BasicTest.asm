
        // push constant 10
        @10
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // push constant 21
        @21
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // push constant 22
        @22
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // push constant 36
        @36
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // push constant 42
        @42
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // push constant 45
        @45
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // push constant 510
        @510
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        

        // push LCL 0
        @0
        D=A
        @LCL
        A=M+D
        D=M
        @SP
        M=D
        @SP
        M=M+1
        

        // push THAT 5
        @5
        D=A
        @THAT
        A=M+D
        D=M
        @SP
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
        D=M+D
        M=D
        @SP
        M=M+1
    

        // push ARG 1
        @1
        D=A
        @ARG
        A=M+D
        D=M
        @SP
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
    

        // push THIS 6
        @6
        D=A
        @THIS
        A=M+D
        D=M
        @SP
        M=D
        @SP
        M=M+1
        

        // push THIS 6
        @6
        D=A
        @THIS
        A=M+D
        D=M
        @SP
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
        D=M+D
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
    

        // push temp 6
        @11
        D=M
        @SP
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
        D=M+D
        M=D
        @SP
        M=M+1
    
