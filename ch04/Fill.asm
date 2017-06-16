  // Fill
  // Fills the screen with black while a key is held
  @8192
  D=A
  @screensize
  M=D
  @i
  M=0
  @drawlocation
  M=0
  @color
  M=0
(GETKEY)
  @i
  M=0
  @KBD
  D=M
  @SETWHITE
  D;JEQ
  @SETBLACK
  0;JMP
(SETWHITE)
  @color
  M=0
  @DRAW
  0;JMP
(SETBLACK)
  @color
  M=-1
  @DRAW
  0;JMP
(DRAW)
  @i             // Get counter
  D=M
  @SCREEN
  D=A+D          // Where to draw
  @drawlocation
  M=D            // Save where to draw
  @color
  D=M
  @drawlocation
  A=M
  M=D            // Draw color
  @i             // Get counter for updating
  D=M
  M=D+1          // Increnent counter
  D=M
  @screensize
  D=D-M          // Have we drawn all the bytes
  @GETKEY
  D;JEQ          // Get Key if we are done drawing
  @DRAW          // Keep drawing
  0;JMP
