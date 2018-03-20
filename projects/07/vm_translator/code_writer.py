def write_arithmetic(operation):
    if operation == 'add':
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n"
    elif operation == 'sub':
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=D-M\n"
    elif operation == 'neg':
        return "@SP\nA=M-1\nM=-M\n"
    elif operation == 'eq':
        return "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@0\nD;JMP\n@16\nD;JEQ\nD=A\n@SP\nA=A-1\nM=D\n"
    elif operation == 'gt':
        return "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@0\nD;JMP\n@16\nD;JGT\nD=A\n@SP\nA=A-1\nM=D\n"
    elif operation == 'lt':
        return "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@0\nD;JMP\n@16\nD;JLT\nD=A\n@SP\nA=A-1\nM=D\n"
    elif operation == 'and':
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\nA=A+1\n"
    elif operation == 'or':
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\nA=A+1\n"
    elif operation =='not':
        return "@SP\nA=A-1\nM=!M\nA=A+1\n"

def write_push(instructions):
    value = instructions['value']
    return "@{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nAM=M+1\n".format(value)

def create_code(instructions):

    def get_assembly_code(instruction):
        if instruction['type'] == 'arithmetic':
            return write_arithmetic(instruction['value'])
        if instruction['type'] == 'push':
            return write_push(instruction['value'])

    code = map(get_assembly_code, instructions)
    return ''.join(str(line) for line in code)
