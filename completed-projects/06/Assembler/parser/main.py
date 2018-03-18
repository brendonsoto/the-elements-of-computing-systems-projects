from binary_dict import symbols


def parse_input(instruction, program_count):

    # Check if the input is a comment or empty space
    if '//' in instruction[0:2] or instruction.isspace():
        return False

    # If we know it's not a newline or empty space, remove the newline char
    instruction = instruction.strip().rstrip('\n')

    # Remove any comments and whitespace in between instruction and comment
    if '//' in instruction:
        comment_start = instruction.index('//')
        instruction = instruction[0:comment_start - 1].strip()

    if '/*' in instruction:
        comment_start = instruction.index('/*')
        instruction = instruction[0:comment_start - 1].strip()

    # Check for parenthesis for a location and tree it like an A-instruction
    if '(' in instruction[0]:
        location = instruction[1:-1]

        # Add the instruction to the symbols for later reference
        symbols.add_entry({ location: program_count })

        # Then return false since we don't want to write this out
        return False

    # Check for the @ symbol to see if it's a A-instruction
    if '@' in instruction[0]:
        address = instruction[1:]
        if address.isdigit():
            address = int(address)
        elif address in symbols.table:
            address = symbols.table[address]
        else:
            symbols.add_entry(address)

        return { 'type': 'A', 'address': address }

    # Let's not worry about error handling much and assume anything at this point is a C instruction 
    comp = 'null'
    dest = 'null'
    jump = 'null'

    # Check if there's some assigning going on
    if '=' in instruction:
        destEndIndex = instruction.find('=')
        dest = instruction[0:destEndIndex]
        comp = instruction[destEndIndex+1:]

    # Otherwise check for a jump
    elif ';' in instruction:
        compEnd = instruction.find(';')
        comp = instruction[:compEnd]
        jump = instruction[compEnd+1:]

    return { 'type': 'C', 'comp': comp, 'dest': dest, 'jump': jump }


def parse_file(asm_file):
    try:
        # Read in and parse the .asm file into a list of dictionaries, each describing each line of the file
        f = open(asm_file, 'r')

        instructions = []
        program_count = 0

        for line in f:

            parsed_input = parse_input(line, program_count)

            if parsed_input is not False:
                instructions.append(parsed_input)
                program_count += 1
        
        f.close()
        return instructions

    except IOError:
        import sys
        print('{0} does not exist. Exiting...'.format(asm_file))
        sys.exit()
