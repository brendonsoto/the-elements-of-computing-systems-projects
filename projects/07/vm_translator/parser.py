def read_file(file_path):
    f = open(file_path, 'r')
    instructions = []

    for line in f:
        if line.isspace() or '//' in line[0:2]:
            continue
        instructions.append(line.strip())

    f.close()
    return instructions

def get_instructions(lines_from_file):
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
    instructions = []

    for line in lines_from_file:
        if line in arithmetic_types:
            instructions.append({ 'type': 'arithmetic', 'value': line })

        words = line.split(' ')
        if words[0] == 'push':
            instructions.append({ 'type': 'push', 'value': { 'type': words[1], 'value': words[2] } })

    return instructions
