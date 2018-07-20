keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']


def tokenize(program_arg, output_type):
    import os, sys

    print(program_arg)
    if os.path.isfile(program_arg) and program_arg.endswith('.jack'):
        tokenize_file(program_arg, output_type)
    elif os.path.isdir(program_arg):
        import glob
        for jack_file in glob.glob("{0}/*.jack".format(program_arg)):
            tokenize_file(jack_file, output_type)


def tokenize_file(jack_file, output_type):
    tokens = get_tokens(jack_file)

    if output_type is 'xml':
        tokens_as_xml = map(get_xml, tokens)
        output_file = jack_file.replace('.jack', '_tokenized.xml')
        write_xml(output_file, tokens_as_xml)
    else:
        output_file = jack_file.replace('.jack', '_tokens')
        write_output(output_file, tokens)


def get_tokens(jack_file):
    tokens = []
    with open(jack_file, 'r') as f:
        for line in f:
            if (not line.isspace() and
                    not line.startswith('//') and
                    not line.startswith('/*') and
                    not line.startswith(' *')):
                code_without_comments = remove_comments(line).strip()
                tokens.extend(get_symbols(code_without_comments))
    return tokens


def remove_comments(line_of_code):
    if '//' in line_of_code:
        return line_of_code[0:line_of_code.index('//') - 1]
    if '/*' in line_of_code:
        return line_of_code[0:line_of_code.index('/*') - 1]
    return line_of_code


'''
get_symbols( string )
returns an array of strings

Iterates through the characters of a line of code to get the tokens associated with the Jack language
'''
def get_symbols(line_of_code):
    symbols_from_code = []
    symbol_parts = [] # to be used per symbol/word
    isCharPartOfString = False
    for char in line_of_code:
        if char == '"' or char == "'":
            if not isCharPartOfString:
                isCharPartOfString = True
            else:
                isCharPartOfString = False
                symbol = "(str){0}".format(''.join(symbol_parts)) # Add a way to identify the token as a string
                symbols_from_code.append(symbol)
                symbol_parts.clear()
        elif char.isspace() and len(symbol_parts) > 0 and not isCharPartOfString:
            symbol = ''.join(symbol_parts)
            symbols_from_code.append(symbol)
            symbol_parts.clear()
        elif char in symbols and not isCharPartOfString:
            if len(symbol_parts) > 0:
                symbol = ''.join(symbol_parts)
                symbols_from_code.append(symbol)
                symbol_parts.clear()
            symbols_from_code.append(char)
        elif not char.isspace() or isCharPartOfString:
            symbol_parts.append(char)
    return symbols_from_code


def get_symbol_code(symbol):
    code = symbol
    if symbol == '<':
        code = '&lt;'
    elif symbol == '>':
        code = '&gt;'
    elif symbol == '&':
        code = '&amp;'
    return code


def get_xml(token):
    xml = ''
    if token in keywords:
        xml = "<keyword> {0} </keyword>".format(token)
    elif token in symbols:
        xml = "<symbol> {0} </symbol>".format(get_symbol_code(token))
    elif "(str)" in token:
        xml = "<stringConstant> {0} </stringConstant>".format(token[5:])
    elif token.isdigit():
        xml = "<integerConstant> {0} </integerConstant>".format(token)
    else:
        xml = "<identifier> {0} </identifier>".format(token)
    return xml


def write_xml(output_file, tokens_as_xml):
    with open(output_file, 'w') as f:
        f.write("<tokens>\n")
        for token in tokens_as_xml:
            f.write(token)
            f.write("\n")
        f.write('</tokens>')
    print("All done writing XML to {0}".format(output_file))

def write_output(output_file, tokens):
    with open(output_file, 'w') as f:
        for token in tokens:
            f.write("{0}\n".format(token))
    print("All done writing XML to {0}".format(output_file))


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 2:
        tokenize(sys.argv[1], sys.argv[2])

    tokenize(sys.argv[1], '')
