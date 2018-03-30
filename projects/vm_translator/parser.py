def remove_inline_comments(vm_command):
    if '//' not in vm_command:
        return vm_command.strip()
    return vm_command[0:vm_command.index('//') - 1].strip()


def get_vm_code_from_file(file_path):
    f = open(file_path, 'r')
    instructions = []

    for line in f:
        if not line.isspace() and not line.startswith('//'):
            command = remove_inline_comments(line)
            instructions.append(command)

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

    # TODO Add this with the rest of the if/elif chain
    if vm_command in arithmetic_commands:
        return { 'type': 'arithmetic', 'value': vm_command }

    parts = vm_command.split(' ')
    instruction = {}

    # Everything is a dict with { type & value } for comment printing
    if parts[0] == 'call':
        instruction = { 'type': 'call', 'value': { 'label': parts[1], 'num_args': int(parts[2]) } }
    elif parts[0] == 'function':
        instruction = { 'type': 'function', 'value': { 'label': parts[1], 'num_args': int(parts[2]) } }
    elif parts[0] == 'goto':
        instruction = { 'type': 'goto', 'value': parts[1] }
    elif parts[0] == 'if-goto':
        instruction = { 'type': 'if-goto', 'value': parts[1] }
    if parts[0] == 'label':
        instruction = { 'type': 'label', 'value': parts[1] }
    elif parts[0] == 'pop':
        instruction = { 'type': 'pop', 'value': { 'base': parts[1], 'index': parts[2] }}
    elif parts[0] == 'push':
        instruction = { 'type': 'push', 'value': { 'type': parts[1], 'value': parts[2] } }
    elif parts[0] == 'return':
        instruction = { 'type': 'return' }

    return instruction


def get_instructions(lines_from_file):
    return map(get_parsed_command, lines_from_file)
