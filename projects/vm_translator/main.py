import code_writer
import parser


def translate_file(vm_file):
    input_code = parser.get_vm_code_from_file(vm_file)
    instructions = parser.get_instructions(input_code)
    return code_writer.create_code(vm_file, instructions)


def compile_vm_files():
    import glob

    # Translate every vm file in the directory
    return "".join(list(map(translate_file, glob.glob("*.vm"))))


def write_asm_out(output, assembly_code):
    code = ''.join([
            code_writer.write_comment({ 'type': 'bootstrap' }),
            code_writer.write_bootstrap(),
            assembly_code
        ])

    f = open(output, 'w')
    f.write(code)
    f.close()
    print('All done writing {0}!'.format(output))


def translate_vm_program(arg):
    import os, sys

    code = ''
    output_file = ''

    # If the argument is a .vm file, process it like norm
    if os.path.isfile(arg) and arg.endswith('.vm'):
        code = translate_file(sys.argv[1])
        output_file = arg.replace('.vm', '.asm')

    # If the arg is a directory, process all of the .vm files in it
    elif os.path.isdir(arg):
        import glob

        # Change directories so we don't have to worry about passing in the path for translate_file calls
        os.chdir(arg)
        code = compile_vm_files()
        file_base = os.path.basename(arg)
        file_name = os.path.splitext(file_base)[0]
        output_file = "{0}.asm".format(file_name)

    else:
        print("{0} is an invalid argument.".format(sys.argv[1]))
        sys.exit()

    write_asm_out(output_file, code)


if __name__ == '__main__':
    import sys
    translate_vm_program(sys.argv[1])
