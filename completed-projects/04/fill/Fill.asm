// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@SCREEN
D=A
@addr
M=D
@value
M=-1



(INPUT)
  @KBD  // Get Keyboard input and save ascii code
  D=M
  @SET_VAL_1 // Set the value to -1 and draw black if there's input
  D;JGT
  @SET_VAL_0 // Otherwise draw white
  D;JMP

(SET_VAL_1)
  @value
  M=-1
  @DRAW
  0;JMP

(SET_VAL_0)
  @value
  M=0
  @DRAW
  0;JMP

(DRAW)
  @value // Get our color (Black or White)
  D=M

  @addr // Go to Address
  A=M   // Switch the address to whatever was in the 'address' variable

  M=D  // Set the 16 bits to 1 (-1)
  A=A+1 // Increment the address by one
  D=A   // Set the Data register to the number of the current register
  
  @addr // Save the incremented address location
  M=D

  @24384// Jump to the end of the screen
  D=D-A // Get the difference of the last address minus this address

  @DRAW
  D;JLT // Jump to the loop if D < 0

  @0
  0;JMP
