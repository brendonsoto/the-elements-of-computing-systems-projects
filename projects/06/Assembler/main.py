from binary_dict import comp, dest, jump, symbols
from parser import main as parser


def synthesize_A_instruction(instructionData):
    address = instructionData['address']
    instruction = address

    if address in symbols.table:
        instruction = symbols.table[address]
    elif not isinstance(address, int):
        instruction = symbols.table[address]

    return "{0:016b}\n".format(instruction);

def synthesize_C_instruction(instructionData):
    compCode = comp.getCode(instructionData['comp'])
    destCode = dest.destCodes[instructionData['dest']]
    jumpCode = jump.jumpCodes[instructionData['jump']]

    return "111{0}{1}{2}\n".format(compCode, destCode, jumpCode)

def write_hack_file(output_file, instructions):
    f = open(output_file, 'w')

    # Now write the instructions out!
    for instruction in instructions:
        binary_code = ''
        if instruction['type'] == 'A':
            binary_code = synthesize_A_instruction(instruction)
        else:
            binary_code = synthesize_C_instruction(instruction)

        f.write(binary_code)

    print('Done writing {0}'.format(output_file))
    f.close()

def main(asm_file):

    # Fill the symbols table up first
    symbols.add_entries_from_file(asm_file)

    # Parse the input into an array of instructions
    instructions = parser.parse_file(asm_file)

    # Write the output file!
    output_file = asm_file.replace('.asm', '.hack')
    write_hack_file(output_file, instructions)


if __name__ == '__main__':
    import sys

    # Print error message if no file was given
    if len(sys.argv) == 1:
        print('Please enter a file as an argument.')
        sys.exit()

    # Get the file to parse from the args
    asm_file = sys.argv[1]
    main(asm_file)
