pointer_address_start = 3
temp_address_start = 5

def get_base_name(vm_memory_keyword):
    bases = {
            'argument': 'ARG',
            'local': 'LCL',
            'that': 'THAT',
            'this': 'THIS',
            }

    if vm_memory_keyword in bases:
        return bases[vm_memory_keyword]

    return vm_memory_keyword


def write_arithmetic(operation, func_end_label):
    code = ''

    if operation == 'add':
        code = "@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n"
    elif operation == 'sub':
        code = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n"
    elif operation == 'neg':
        code = "@SP\nA=M-1\nM=-M\n"
    elif operation == 'eq':
        code = ("@{0}\nD=A\n@R13\nM=D\n"
                "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n"
                "@SET_BOOL_TRUE\nD;JEQ\n@SET_BOOL_FALSE\nD;JMP\n({0})\n").format(func_end_label)
    elif operation == 'gt':
        code = ("@{0}\nD=A\n@R13\nM=D\n"
                "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n"
                "@SET_BOOL_TRUE\nD;JGT\n@SET_BOOL_FALSE\nD;JMP\n({0})\n").format(func_end_label)
    elif operation == 'lt':
        code = ("@{0}\nD=A\n@R13\nM=D\n"
                "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n"
                "@SET_BOOL_TRUE\nD;JLT\n@SET_BOOL_FALSE\nD;JMP\n({0})\n").format(func_end_label)
    elif operation == 'and':
        code = "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\nA=A+1\n"
    elif operation == 'or':
        code = "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\nA=A+1\n"
    elif operation =='not':
        code = "@SP\nA=M-1\nM=!M\nA=A+1\n"

    return code


def write_comment(instruction):
    if 'value' not in instruction:
        return "// {0}\n".format(instruction['type'])
    if type(instruction['value']) is dict:
        dict_values = ' '.join(instruction['value'].values())
        return "// {0} {1}\n".format(instruction['type'], dict_values)
    return "// {0} {1}\n".format(instruction['type'], instruction['value'])


def write_function_declaration(label, num_args):
    code = []
    code.append("({0})\n".format(label))

    for i in range(num_args):
        code.append(write_push({ 'type': 'constant', 'value': '0' }))

    return "".join(code)

def write_function_return():
    return ''.join([
        "@LCL\nD=M\n@R5\nM=D\n", # FRAME = LCL
        "@5\nD=A\n@LCL\nD=M-D\n@R6\nM=D\n", # Return address = FRAME - 5
        write_pop({ 'base': 'argument', 'index': 0 }), # Pop into ARG
        "@ARG\nD=M+1\n@SP\nM=D\n", # SP = ARG + 1
        "@R5\nA=M-1\nD=M\n@THAT\nM=D\n", # THAT = FRAME - 1
        "@2\nD=A\n@R5\nA=M-D\nD=M\n@THIS\nM=D\n", # THIS = FRAME - 2
        "@3\nD=A\n@R5\nA=M-D\nD=M\n@ARG\nM=D\n", # ARG = FRAME - 3
        "@4\nD=A\n@R5\nA=M-D\nD=M\n@LCL\nM=D\n", # LCL = FRAME - 4
        write_goto("@R6\nA=M")
    ])

def write_goto(label):
    return "{0}\nD;JMP\n".format(label)


# FIXME Duplication of file_name
def write_if(vm_file, label):
    import os
    file_base = os.path.basename(vm_file)
    file_name = os.path.splitext(file_base)[0]
    return "@SP\nAM=M-1\nD=M\n@{0}.{1}\nD;JGT\n".format(file_name, label)


def write_label(vm_file, label):
    import os
    file_base = os.path.basename(vm_file)
    file_name = os.path.splitext(file_base)[0]
    return "({0}.{1})\n".format(file_name, label)


# The helpers are surrounded by END statements/declaration because they will be added at the end and we don't want the helpers to be run at the end of the program
def write_helpers():
    with open('./HELPERS', 'r') as f:
        return f.read()


def write_pop(instruction):
    index_from_base = instruction['index']
    pop_code = ''

    if instruction['base'] == 'pointer':
        pop_code = "@SP\nAM=M-1\nD=M\n@R{0}\nM=D\n".format(pointer_address_start + int(index_from_base))
    elif instruction['base'] == 'static':
        pop_code = "@SP\nAM=M-1\nD=M\n@static.{0}\nM=D\n".format(index_from_base)
    elif instruction['base'] == 'temp':
        pop_code = "@SP\nAM=M-1\nD=M\n@R{0}\nM=D\n".format(temp_address_start + int(index_from_base))
    elif index_from_base == '0':
        base_address = get_base_name(instruction['base'])
        pop_code = "@SP\nAM=M-1\nD=M\n@{0}\nA=M\nM=D\n".format(base_address)
    else:
        base_address = get_base_name(instruction['base'])
        address_register = 'A' if instruction['base'] == 'temp' else 'M'
        pop_code = ("@{0}\nD={1}\n@{2}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
                .format(base_address, address_register, index_from_base))

    return pop_code


def write_push(instruction):
    value = instruction['value']
    push_code = ''

    if instruction['type'] == 'constant':
        push_code = "@{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nAM=M+1\n".format((instruction['value']))
    elif instruction['type'] == 'pointer':
        push_code = "@R{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(pointer_address_start + int(value))
    elif instruction['type'] == 'static':
        push_code = "@static.{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(value)
    elif instruction['type'] == 'temp':
        push_code = "@R{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(temp_address_start + int(value))
    elif value == '0':
        base = get_base_name(instruction['type'])
        push_code = "@{0}\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(base)
    else:
        base = get_base_name(instruction['type'])
        push_code = "@{0}\nA=M\nD=A\n@{1}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(base, value)

    return push_code


def check_if_helpers_are_needed(instructions):
    for instruction in instructions:
        if (instruction['value'] == 'eq' or
            instruction['value'] == 'gt' or
            instruction['value'] == 'lt'):
            return True
    return False


def create_code(vm_file, instructions):
    equality_func_count = 0

    code = []
    for instruction in instructions:

        # Add comments dynamically
        code.append(write_comment(instruction))

        if instruction['type'] == 'arithmetic':
            import os
            file_base = os.path.basename(vm_file)
            file_name = os.path.splitext(file_base)[0]
            func_end_label = "{0}.arith_func_{1}".format(file_name, equality_func_count)
            code.append(write_arithmetic(instruction['value'], func_end_label))
            equality_func_count += 1

        if instruction['type'] == 'push':
            code.append(write_push(instruction['value']))
        elif instruction['type'] == 'pop':
            code.append(write_pop(instruction['value']))
        elif instruction['type'] == 'function':
            code.append(
                    write_function_declaration(
                        instruction['value']['label'],
                        int(instruction['value']['num_args']
                    )
                )
            )
        elif instruction['type'] == 'goto':
            import os
            file_base = os.path.basename(vm_file)
            file_name = os.path.splitext(file_base)[0]
            label = "@{0}.{1}".format(file_name, instruction['value'])
            code.append(write_goto(label))
        elif instruction['type'] == 'if-goto':
            code.append(write_if(vm_file, instruction['value']))
        elif instruction['type'] == 'label':
            code.append(write_label(vm_file, instruction['value']))
        elif instruction['type'] == 'return':
            code.append(write_function_return())

    are_helpers_needed = check_if_helpers_are_needed(instructions)

    if are_helpers_needed:
        code.append(write_helpers())

    return ''.join(code)
