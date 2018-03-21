def write_arithmetic(operation, func_end_label):
    if operation == 'add':
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n"
    elif operation == 'sub':
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n"
    elif operation == 'neg':
        return "@SP\nA=M-1\nM=-M\n"
    elif operation == 'eq':
        return ("@{0}\nD=A\n@R5\nM=D\n"
                "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n"
                "@SET_BOOL_TRUE\nD;JEQ\n@SET_BOOL_FALSE\nD;JMP\n({0})\n").format(func_end_label)
    elif operation == 'gt':
        return ("@{0}\nD=A\n@R5\nM=D\n"
                "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n"
                "@SET_BOOL_TRUE\nD;JGT\n@SET_BOOL_FALSE\nD;JMP\n({0})\n").format(func_end_label)
    elif operation == 'lt':
        return ("@{0}\nD=A\n@R5\nM=D\n"
                "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n"
                "@SET_BOOL_TRUE\nD;JLT\n@SET_BOOL_FALSE\nD;JMP\n({0})\n").format(func_end_label)
    elif operation == 'and':
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\nA=A+1\n"
    elif operation == 'or':
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\nA=A+1\n"
    elif operation =='not':
        return "@SP\nA=M-1\nM=!M\nA=A+1\n"

# The helpers are surrounded by END statements/declaration because they will be added at the end and we don't want the helpers to be run at the end of the program
def write_helpers():
    end_jump = "@END\nD;JMP\n"
    set_bool_true_routine = "(SET_BOOL_TRUE)\n@SP\nA=M\nM=-1\n@SP\nAM=M+1\n@R5\nA=M\nD;JMP\n"
    set_bool_false_routine = "(SET_BOOL_FALSE)\n@SP\nA=M\nM=0\n@SP\nAM=M+1\n@R5\nA=M\nD;JMP\n"
    end_declaration = "(END)\n"
    return ''.join([end_jump, set_bool_true_routine, set_bool_false_routine, end_declaration])

def check_if_helpers_are_needed(instructions):
    for instruction in instructions:
        if instruction['value'] == 'eq' or instruction['value'] == 'gt' or instruction['value'] == 'lt':
            return True
    return False

def write_push(instructions):
    value = instructions['value']
    return "@{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nAM=M+1\n".format(value)

def create_code(instructions):
    equality_func_count = 0

    code = []
    for instruction in instructions:
        if instruction['type'] == 'arithmetic':
            func_end_label = "arith_func_{0}".format(equality_func_count)
            code.append(write_arithmetic(instruction['value'], func_end_label))
            equality_func_count += 1
        if instruction['type'] == 'push':
            code.append(write_push(instruction['value']))

    are_helpers_needed = check_if_helpers_are_needed(instructions)
    if are_helpers_needed:
        code.append(write_helpers())

    return ''.join(code)
