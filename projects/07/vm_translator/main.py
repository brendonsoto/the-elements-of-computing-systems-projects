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
    import sys
    vm_file = sys.argv[1]
    translate_file(vm_file)
