def read_file(file_path):
    f = open(file_path, 'r')
    instructions = []

    for line in f:
        if line.isspace() or '//' in line[0:2]:
            continue
        instructions.append(line.strip())

    f.close()
    return instructions

def translate_line(line):
    arithmetic_types = [
            'add',
            'sub',
            'neg',
            'eq',
            'gt',
            'lt',
            'and',
            'or',
            'not'
            ]

    if line in arithmetic_types:
        return { 'type': 'arithmetic', 'value': line }

    words = line.split(' ')
    instruction = {}

    if words[0] == 'push':
        instruction = { 'type': 'push', 'value': { 'type': words[1], 'value': words[2] } }
    if words[0] == 'pop':
        instruction = { 'type': 'pop', 'value': { 'base': words[1], 'index': words[2] }}

    return instruction

def get_instructions(lines_from_file):

    instructions = []

    for line in lines_from_file:
        instructions.append(translate_line(line))

    return instructions
