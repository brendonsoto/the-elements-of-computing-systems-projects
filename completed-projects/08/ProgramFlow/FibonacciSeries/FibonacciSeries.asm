// push argument 1
@ARG
A=M
D=A
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
AM=M-1
D=M
@R4
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
AM=M+1
// pop that 0
@SP
AM=M-1
D=M
@THAT
A=M
M=D
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
AM=M+1
// pop that 1
@THAT
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
AM=M+1
// arithmetic sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// pop argument 0
@SP
AM=M-1
D=M
@ARG
A=M
M=D
// label MAIN_LOOP_START
(FibonacciSeries.MAIN_LOOP_START)
// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto COMPUTE_ELEMENT
@SP
AM=M-1
D=M
@FibonacciSeries.COMPUTE_ELEMENT
D;JGT
// goto END_PROGRAM
@FibonacciSeries.END_PROGRAM
D;JMP
// label COMPUTE_ELEMENT
(FibonacciSeries.COMPUTE_ELEMENT)
// push that 0
@THAT
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that 1
@THAT
A=M
D=A
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// arithmetic add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// pop that 2
@THAT
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push pointer 1
@R4
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
AM=M+1
// arithmetic add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// pop pointer 1
@SP
AM=M-1
D=M
@R4
M=D
// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
AM=M+1
// arithmetic sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// pop argument 0
@SP
AM=M-1
D=M
@ARG
A=M
M=D
// goto MAIN_LOOP_START
@FibonacciSeries.MAIN_LOOP_START
D;JMP
// label END_PROGRAM
(FibonacciSeries.END_PROGRAM)
