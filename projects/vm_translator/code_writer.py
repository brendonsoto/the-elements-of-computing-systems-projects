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
        code = ("@{0}\nD=A\n@R13\nM=D\n" # Save return address
                "@SP\nAM=M-1\nD=M\nA=A-1\nMD=M-D\n" # Get bool val
                "@SET_BOOL_TRUE\nD;JEQ\n@SET_BOOL_FALSE\nD;JMP\n({0})\n").format(func_end_label)
    elif operation == 'gt':
        code = ("@{0}\nD=A\n@R13\nM=D\n" # Save return address
                "@SP\nAM=M-1\nD=M\nA=A-1\nMD=M-D\n" # Get bool val
                "@SET_BOOL_TRUE\nD;JGT\n@SET_BOOL_FALSE\nD;JMP\n({0})\n").format(func_end_label)
    elif operation == 'lt':
        code = ("@{0}\nD=A\n@R13\nM=D\n" # Save return address
                "@SP\nAM=M-1\nD=M\nA=A-1\nMD=M-D\n" # Get bool val
                "@SET_BOOL_TRUE\nD;JLT\n@SET_BOOL_FALSE\nD;JMP\n({0})\n").format(func_end_label)
    elif operation == 'and':
        code = "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\nA=A+1\n"
    elif operation == 'or':
        code = "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\nA=A+1\n"
    elif operation =='not':
        code = "@SP\nA=M-1\nM=!M\nA=A+1\n"

    return code


def write_bootstrap():
    return ''.join([
            "@256\nD=A\n@SP\nM=D\n", # Init SP to RAM[256]
            write_function_call("Sys.init", 0, "Sys.init_return")
            ])


def write_comment(instruction):
    if 'value' not in instruction:
        return "// {0}\n".format(instruction['type'])
    if type(instruction['value']) is dict:
        dict_values = ' '.join(str(val) for val in instruction['value'].values())
        return "// {0} {1}\n".format(instruction['type'], dict_values)
    return "// {0} {1}\n".format(instruction['type'], instruction['value'])


# function_label = (for example) Sys.init
def write_function_call(function_label, num_args, return_address):
    arg_pointer_offset = num_args + 5
    return ''.join([
        write_push({ 'type': 'address', 'value': return_address }), # Push return address
        write_push({ 'type': 'memory', 'value': 'local' }), # Push LCL 
        write_push({ 'type': 'memory', 'value': 'argument' }), # Push ARG
        write_push({ 'type': 'memory', 'value': 'this' }), # Push THIS
        write_push({ 'type': 'memory', 'value': 'that' }), # push THAT
        "@SP\nD=M\n@{0}\nD=D-A\n@ARG\nM=D\n".format(arg_pointer_offset), # ARG = SP - n - 5
        "@SP\nD=M\n@LCL\nM=D\n", # LCL = SP
        write_goto("@{0}".format(function_label)), # Goto function
        "({0})\n".format(return_address) # Write Return Label -- Not using func since label includes file
        ])


def write_function_declaration(label, num_args):
    code = []
    code.append("({0})\n".format(label))

    for i in range(num_args):
        code.append(write_push({ 'type': 'constant', 'value': '0' }))

    return "".join(code)


def write_function_return():
    return ''.join([
        "@LCL\nD=M\n@R5\nM=D\n", # FRAME = LCL
        "@5\nD=A\n@LCL\nA=M-D\nD=M\n@R6\nM=D\n", # Return address = FRAME - 5
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


def write_if(file_name, label):
    return "@SP\nAM=M-1\nD=M\n@{0}.{1}\nD;JLT\n".format(file_name, label)


def write_label(file_name, label):
    return "({0}.{1})\n".format(file_name, label)


# The helpers are surrounded by END statements/declaration because they will be added at the end and we don't want the helpers to be run at the end of the program
def write_helpers():
    import os

    code = ''

    # Switch temporarily to the VM Translator dir to get the Helpers
    orig_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    with open('./HELPERS', 'r') as f:
        code = f.read()

    os.chdir(orig_dir)
    return code


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


# TODO Abstract out common strings (i.e. incrementing SP)
def write_push(instruction):
    push_code = ''

    if instruction['type'] == 'address':
        push_code = "@{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(instruction['value'])
    elif instruction['type'] == 'constant':
        push_code = "@{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nAM=M+1\n".format(instruction['value'])
    elif instruction['type'] == 'memory':
        memory_keyword = get_base_name(instruction['value'])
        push_code = "@{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(memory_keyword)
    elif instruction['type'] == 'pointer':
        push_code = "@R{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(pointer_address_start + int(instruction['value']))
    elif instruction['type'] == 'static':
        push_code = "@static.{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(instruction['value'])
    elif instruction['type'] == 'temp':
        push_code = "@R{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(temp_address_start + int(instruction['value']))
    elif instruction['value'] == '0':
        base = get_base_name(instruction['type'])
        push_code = "@{0}\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(base)
    else:
        base = get_base_name(instruction['type'])
        push_code = "@{0}\nA=M\nD=A\n@{1}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(base, instruction['value'])

    return push_code


def create_code(vm_file, instructions):
    equality_func_count = 0
    func_call_count = 0

    code = []
    for instruction in instructions:

        if 'type' not in instruction:
            continue

        # Add comments dynamically
        code.append(write_comment(instruction))

        if instruction['type'] == 'push':
            code.append(write_push(instruction['value']))
        elif instruction['type'] == 'pop':
            code.append(write_pop(instruction['value']))
        elif instruction['type'] == 'call':
            return_address = "{0}.{1}_return_{2}".format(vm_file, instruction['value']['label'], func_call_count)
            code.append(write_function_call(
                instruction['value']['label'],
                instruction['value']['num_args'],
                return_address
                ))
            func_call_count += 1
        elif instruction['type'] == 'function':
            code.append(
                    write_function_declaration(
                        instruction['value']['label'],
                        instruction['value']['num_args']
                        )
                    )
        elif instruction['type'] == 'return':
            code.append(write_function_return())
        else:

            # These are all instruction types that need the file name since they all involve labels
            import os
            file_base = os.path.basename(vm_file)
            file_name = os.path.splitext(file_base)[0]

            if instruction['type'] == 'arithmetic':
                func_end_label = "{0}.arith_func_{1}".format(file_name, equality_func_count)
                code.append(write_arithmetic(instruction['value'], func_end_label))
            elif instruction['type'] == 'goto':
                label = "@{0}.{1}".format(file_name, instruction['value'])
                code.append(write_goto(label))
            elif instruction['type'] == 'if-goto':
                code.append(write_if(file_name, instruction['value']))
            elif instruction['type'] == 'label':
                code.append(write_label(file_name, instruction['value']))

    return ''.join(code)
