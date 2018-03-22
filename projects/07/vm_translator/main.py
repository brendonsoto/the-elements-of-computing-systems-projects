import code_writer
import parser


def translate_file(vm_file):
    input_code = parser.read_file(vm_file)
    instructions = parser.get_instructions(input_code)
    assembly_code = code_writer.create_code(instructions)

    output = vm_file.replace('.vm', '.asm')
    f = open(output, 'w')
    f.write(assembly_code)
    f.close()
    print('All done writing {0}!'.format(output))

if __name__ == '__main__':
    import os, sys

    # If the argument is a .vm file, process it like norm
    if os.path.isfile(sys.argv[1]) and sys.argv[1].endswith('.vm'):
        vm_file = sys.argv[1]
        translate_file(vm_file)

    # If the arg is a directory, process all of the .vm files in it
    elif os.path.isdir(sys.argv[1]):
        import glob

        # Change directories so we don't have to worry about passing in the path for translate_file calls
        os.chdir(sys.argv[1])
        for file in glob.glob("*.vm"):
            translate_file(file)

    else:
        print("{0} is an invalid argument.".format(sys.argv[1]))
