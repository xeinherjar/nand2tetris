// Multiplication
// Arg1 = R0
// Arg2 = R1
// Product = R2
// Where R0 and R1 >=0 and R2 = R0 * R1
  @R0
  D=M
  @n         // Number to multiply
  M=D
  @R1
  D=M
  @i         // Number of iterations
  M=D
  @R2
  M=0
(LOOP)
  @i         // Number of iterations left
  D=M
  @END
  D;JEQ      // Jump to end if we have reached 0
  @n
  D=M
  @R2
  D=M+D      // Do Math
  M=D        // Store result
  @i
  M=M-1     // Remove one from iteration counter
  @LOOP
  0;JMP
(END)
  @END
  0;JMP
