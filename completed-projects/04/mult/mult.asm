// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@2
M=0 // Product
(LOOP)
  @0    // Use RAM[0] as our countdown
  D=M   // Grab our counter
  @END  // Navigate to the end portion of the program
  D;JEQ // If D=0, jump to the end
  @1
  D=M
  @2
  M=D+M
  @0
  M=M-1
  @LOOP
  0;JMP
(END)
  @END
  0;JMP
