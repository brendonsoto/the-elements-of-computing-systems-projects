// bootstrap
@256
D=A
@SP
M=D
@Sys.init_return
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
D;JMP
(Sys.init_return)
// function Class1.vm Class1.set 0
(Class1.set)
// push Class1.vm argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop Class1.vm static 0
@SP
AM=M-1
D=M
@Class1.vm.static.0
M=D
// push Class1.vm argument 1
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
// pop Class1.vm static 1
@SP
AM=M-1
D=M
@Class1.vm.static.1
M=D
// push Class1.vm constant 0
@0
D=A
@SP
A=M
M=D
@SP
AM=M+1
// return
@LCL
D=M
@R5
M=D
@5
D=A
@LCL
A=M-D
D=M
@R6
M=D
@ARG
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
@ARG
D=M+1
@SP
M=D
@R5
A=M-1
D=M
@THAT
M=D
@2
D=A
@R5
A=M-D
D=M
@THIS
M=D
@3
D=A
@R5
A=M-D
D=M
@ARG
M=D
@4
D=A
@R5
A=M-D
D=M
@LCL
M=D
@R6
A=M
D;JMP
// function Class1.vm Class1.get 0
(Class1.get)
// push Class1.vm static 0
@Class1.vm.static.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push Class1.vm static 1
@Class1.vm.static.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// arithmetic sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// return
@LCL
D=M
@R5
M=D
@5
D=A
@LCL
A=M-D
D=M
@R6
M=D
@ARG
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
@ARG
D=M+1
@SP
M=D
@R5
A=M-1
D=M
@THAT
M=D
@2
D=A
@R5
A=M-D
D=M
@THIS
M=D
@3
D=A
@R5
A=M-D
D=M
@ARG
M=D
@4
D=A
@R5
A=M-D
D=M
@LCL
M=D
@R6
A=M
D;JMP
// function Class2.vm Class2.set 0
(Class2.set)
// push Class2.vm argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop Class2.vm static 0
@SP
AM=M-1
D=M
@Class2.vm.static.0
M=D
// push Class2.vm argument 1
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
// pop Class2.vm static 1
@SP
AM=M-1
D=M
@Class2.vm.static.1
M=D
// push Class2.vm constant 0
@0
D=A
@SP
A=M
M=D
@SP
AM=M+1
// return
@LCL
D=M
@R5
M=D
@5
D=A
@LCL
A=M-D
D=M
@R6
M=D
@ARG
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
@ARG
D=M+1
@SP
M=D
@R5
A=M-1
D=M
@THAT
M=D
@2
D=A
@R5
A=M-D
D=M
@THIS
M=D
@3
D=A
@R5
A=M-D
D=M
@ARG
M=D
@4
D=A
@R5
A=M-D
D=M
@LCL
M=D
@R6
A=M
D;JMP
// function Class2.vm Class2.get 0
(Class2.get)
// push Class2.vm static 0
@Class2.vm.static.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push Class2.vm static 1
@Class2.vm.static.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// arithmetic sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// return
@LCL
D=M
@R5
M=D
@5
D=A
@LCL
A=M-D
D=M
@R6
M=D
@ARG
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
@ARG
D=M+1
@SP
M=D
@R5
A=M-1
D=M
@THAT
M=D
@2
D=A
@R5
A=M-D
D=M
@THIS
M=D
@3
D=A
@R5
A=M-D
D=M
@ARG
M=D
@4
D=A
@R5
A=M-D
D=M
@LCL
M=D
@R6
A=M
D;JMP
// function Sys.vm Sys.init 0
(Sys.init)
// push Sys.vm constant 6
@6
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push Sys.vm constant 8
@8
D=A
@SP
A=M
M=D
@SP
AM=M+1
// call Sys.vm Class1.set 2
@Sys.vm.Class1.set_return_0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@7
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
D;JMP
(Sys.vm.Class1.set_return_0)
// pop Sys.vm temp 0
@SP
AM=M-1
D=M
@R5
M=D
// push Sys.vm constant 23
@23
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push Sys.vm constant 15
@15
D=A
@SP
A=M
M=D
@SP
AM=M+1
// call Sys.vm Class2.set 2
@Sys.vm.Class2.set_return_1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@7
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
D;JMP
(Sys.vm.Class2.set_return_1)
// pop Sys.vm temp 0
@SP
AM=M-1
D=M
@R5
M=D
// call Sys.vm Class1.get 0
@Sys.vm.Class1.get_return_2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
D;JMP
(Sys.vm.Class1.get_return_2)
// call Sys.vm Class2.get 0
@Sys.vm.Class2.get_return_3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
D;JMP
(Sys.vm.Class2.get_return_3)
// label WHILE
(Sys.WHILE)
// goto WHILE
@Sys.WHILE
D;JMP
