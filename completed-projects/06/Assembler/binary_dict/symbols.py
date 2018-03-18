table = {
        '_address': 16,
        'ARG': 2,
        'KBD': 24576,
        'LCL': 1,
        'R0': 0,
        'R1': 1,
        'R10': 10,
        'R11': 11,
        'R12': 12,
        'R13': 13,
        'R14': 14,
        'R15': 15,
        'R2': 2,
        'R3': 3,
        'R4': 4,
        'R5': 5,
        'R6': 6,
        'R7': 7,
        'R8': 8,
        'R9': 9,
        'SCREEN': 16384,
        'SP': 0,
        'THAT': 4,
        'THIS': 3
        }


def add_entry(instruction):
    if isinstance(instruction, str):
        table[instruction] = table['_address']
        table['_address'] += 1
    elif isinstance(instruction, dict):

        # The dict should only have 1 entry so get it
        key = next(iter(instruction))
        table[key] = instruction[key]
    else:
        error = 'Invalid instruction for the user symbols table. Type {0} given'.format(type(instruction))
        raise ValueError('Invalid instruction for the user symbols table')

# Add symbols from a file to the symbols table -- assumes file exists and is of right filetype
def add_entries_from_file(asm_file):
    try:
        if asm_file[-4:] != '.asm':
            raise ValueError('Incorrect file type entered') 

        f = open(asm_file, 'r')

        program_count = 0

        for line in f:
            if '//' in line[0:2] or line.isspace():
                continue
            elif '(' in line[0]:
                location = line.strip()[1:-1]
                add_entry({ location: program_count })
            else:
                program_count += 1

        f.close()
    except IOError:
        import sys
        print('{0} does not exist. Exiting...'.format(asm_file))
        sys.exit()
