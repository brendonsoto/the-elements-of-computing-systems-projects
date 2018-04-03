// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
AM=M+1
// pop local 0
@SP
AM=M-1
D=M
@LCL
A=M
M=D
// label LOOP_START
(BasicLoop.LOOP_START)
// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 0
@LCL
A=M
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
// pop local 0	
@LCL
D=M
@0	
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
// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto LOOP_START
@SP
AM=M-1
D=M
@BasicLoop.LOOP_START
D;JGT
// push local 0
@LCL
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
