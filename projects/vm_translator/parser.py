def get_vm_code_from_file(file_path):
    f = open(file_path, 'r')
    instructions = []

    for line in f:
        if not line.isspace() and not line.startswith('//'):
            instructions.append(line.strip())

    f.close()
    return instructions


def get_parsed_command(vm_command):
    arithmetic_commands = [
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

    if vm_command in arithmetic_commands:
        return { 'type': 'arithmetic', 'value': vm_command }

    parts = vm_command.split(' ')
    instruction = {}

    if parts[0] == 'push':
        # Everything is a dict with { type & value } for comment printing
        instruction = { 'type': 'push', 'value': { 'type': parts[1], 'value': parts[2] } }
    elif parts[0] == 'pop':
        instruction = { 'type': 'pop', 'value': { 'base': parts[1], 'index': parts[2] }}
    elif parts[0] == 'label':
        instruction = { 'type': 'label', 'value': parts[1] }
    elif parts[0] == 'function':
        instruction = { 'type': 'function', 'value': { 'label': parts[1], 'num_args': parts[2] } }
    elif parts[0] == 'goto':
        instruction = { 'type': 'goto', 'value': parts[1] }
    elif parts[0] == 'if-goto':
        instruction = { 'type': 'if-goto', 'value': parts[1] }
    elif parts[0] == 'return':
        instruction = { 'type': 'return' }

    return instruction


def get_instructions(lines_from_file):
    return map(get_parsed_command, lines_from_file)
