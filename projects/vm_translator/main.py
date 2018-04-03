import code_writer
import parser


def translate_file(vm_file):
    input_code = parser.get_vm_code_from_file(vm_file)
    instructions = parser.get_instructions(vm_file, input_code)
    return code_writer.create_code(vm_file, instructions)


def check_if_helpers_are_needed(vm_file):
    with open(vm_file, 'r') as f:
        are_helpers_needed = False
        for line in f:
            if 'eq' in line or 'gt' in line or 'lt' in line:
                are_helpers_needed = True
                break
        return are_helpers_needed


def check_if_directory_needs_helpers(directory_path):
    import glob

    are_helpers_needed = False
    for vm_file in glob.glob("*.vm"):
        if check_if_helpers_are_needed(vm_file):
            are_helpers_needed = True
            break
    return are_helpers_needed


def compile_vm_files():
    import glob

    # Translate every vm file in the directory
    code = map(translate_file, glob.glob("*.vm"))
    return "".join(list(code))


def write_asm_out(output, assembly_code, are_helpers_needed):
    code = ''.join([
            code_writer.write_comment({ 'type': 'bootstrap' }),
            code_writer.write_bootstrap(),
            assembly_code,
            code_writer.write_helpers() if are_helpers_needed else ''
        ])

    f = open(output, 'w')
    f.write(code)
    f.close()
    print('All done writing {0}!'.format(output))


def translate_vm_program(arg):
    import os, sys

    code = ''
    output_file = ''
    are_helpers_needed = False

    # If the argument is a .vm file, process it like norm
    if os.path.isfile(arg) and arg.endswith('.vm'):
        are_helpers_needed = check_if_helpers_are_needed(sys.argv[1])
        code = translate_file(sys.argv[1])
        output_file = arg.replace('.vm', '.asm')

    # If the arg is a directory, process all of the .vm files in it
    elif os.path.isdir(arg):
        import glob

        directory_path = os.path.normpath(arg)

        # Change directories so we don't have to worry about passing in the path for translate_file calls
        os.chdir(directory_path)

        are_helpers_needed = check_if_directory_needs_helpers("./")

        code = compile_vm_files()
        directory_name = os.path.split(directory_path)[1]
        output_file = "{0}.asm".format(directory_name)

    else:
        print("{0} is an invalid argument.".format(sys.argv[1]))
        sys.exit()

    write_asm_out(output_file, code, are_helpers_needed)


if __name__ == '__main__':
    import sys
    translate_vm_program(sys.argv[1])
