# NOTE Post-Proj-7: I don't like global variables much. This probably could've been encapsulated inside a function (i.e. `get_base_name`)
bases = {
        'argument': 'ARG',
        'local': 'LCL',
        'pointer': 'R3',
        'static': 'static',
        'temp': 'R5',
        'that': 'THAT',
        'this': 'THIS',
        }


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


# NOTE Post-Proj-7: This still urks me a bit, but I don't know how to clean it up. It's basically outputting a simple string.
# Maybe it would've been better to just have a separate text file with the routine and have a function call to grab the file and insert the text?
# The helpers are surrounded by END statements/declaration because they will be added at the end and we don't want the helpers to be run at the end of the program
def write_helpers():
    end_jump = "@END\nD;JMP\n"
    set_bool_true_routine = "(SET_BOOL_TRUE)\n@SP\nA=M\nM=-1\n@SP\nAM=M+1\n@R13\nA=M\nD;JMP\n"
    set_bool_false_routine = "(SET_BOOL_FALSE)\n@SP\nA=M\nM=0\n@SP\nAM=M+1\n@R13\nA=M\nD;JMP\n"
    end_declaration = "(END)\n"

    return ''.join([
        end_jump,
        set_bool_true_routine,
        set_bool_false_routine,
        end_declaration
        ])


def check_if_helpers_are_needed(instructions):
    for instruction in instructions:
        if (instruction['value'] == 'eq' or
            instruction['value'] == 'gt' or
            instruction['value'] == 'lt'):
            return True
    return False


# NOTE Post-Proj-7: For temp and pointer, I probably could've avoided calling format twice by calculating the address as an int and jsut feeding that into the pop_code format func. Same with Static actually.
def write_pop(instruction):
    index_from_base = instruction['index']
    pop_code = ''

    if instruction['base'] == 'pointer':
        address = 'R{0}'.format(3+int(index_from_base))
        pop_code = "@SP\nAM=M-1\nD=M\n@{0}\nM=D\n".format(address)

    elif instruction['base'] == 'static':
        address = 'static.{0}'.format(index_from_base)
        pop_code = "@SP\nAM=M-1\nD=M\n@{0}\nM=D\n".format(address)

    elif instruction['base'] == 'temp':
        address = 'R{0}'.format(5+int(index_from_base))
        pop_code = "@SP\nAM=M-1\nD=M\n@{0}\nM=D\n".format(address)

    elif index_from_base == '0':
        base_address = bases[instruction['base']]
        pop_code = "@SP\nAM=M-1\nD=M\n@{0}\nA=M\nM=D\n".format(base_address)

    else:
        base_address = bases[instruction['base']]
        address_register = 'A' if instruction['base'] == 'temp' else 'M'
        pop_code = ("@{0}\nD={1}\n@{2}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
                .format(base_address, address_register, index_from_base))

    return pop_code


def write_push_constant(value):
    return "@{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nAM=M+1\n".format(value)


# NOTE Post-Proj-7: Pop comments apply here too.
def write_push(instruction):
    value = instruction['value']
    push_code = ''

    if instruction['type'] == 'constant':
        push_code = write_push_constant(instruction['value'])

    elif instruction['type'] == 'pointer':
        address = "R{0}".format(3+int(value))
        push_code = "@{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(address)

    elif instruction['type'] == 'static':
        address = "static.{0}".format(value)
        push_code = "@{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(address)

    elif instruction['type'] == 'temp':
        address = "R{0}".format(5+int(value))
        push_code = "@{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(address)

    elif value == '0':
        base = bases[instruction['type']]
        push_code = "@{0}\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(base)

    else:
        base = bases[instruction['type']]
        push_code = "@{0}\nA=M\nD=A\n@{1}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(base, value)

    return push_code


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

        if instruction['type'] == 'pop':
            code.append(write_pop(instruction['value']))

    are_helpers_needed = check_if_helpers_are_needed(instructions)

    if are_helpers_needed:
        code.append(write_helpers())

    return ''.join(code)
