from ClassDescriptor import get_class_description
from TokenIterator import TokenIterator
import XMLConverter


def compile_input(command_arg):
    import os, sys
    if os.path.isfile(command_arg):
        print(get_compiled_output(command_arg))
    elif os.path.isdir(command_arg):
        import glob
        for jack_file in glob.glob("{0}/*.jack".format(command_arg)):
            get_compiled_output(jack_file)

'''
get_compiled_output
input: tokens -- an array of strings
output: a graph/tree of tokens
opt output: XML
'''
def get_compiled_output(tokens_file):
    tokens = []

    with open(tokens_file, 'r') as f:
        for line in f:
            tokens.append(line.strip())

    token_iterator = TokenIterator(tokens)

    jack_class = get_class_description(token_iterator)

    # output(jack_class, 'xml')
    return output(jack_class, 'test')
    # return output(jack_class, 'xml')


def output(jack_class, output_type):
    if output_type is 'test':
        return jack_class

    if output_type != 'xml':
        raise ValueError('Incorrect output type received. Available types: xml')

    if output_type is 'xml':
        print('Main -- outputting xml\n\n')
        return XMLConverter.convert_class(jack_class)




def test():
    tokens = [
            'class',
            'Main',
            '{',
            'field',
            'int',
            'count',
            ',',
            'current',
            ';',
            'static',
            'boolean',
            'isLoading',
            'hasMore',
            'isEmpty',
            ';',
            'function',
            'void',
            'main',
            '(',
            'int',
            'count',
            ',',
            'boolean',
            'isTrue',
            ')',
            '{',
            'var',
            'int',
            'temp',
            ';',
            'let',
            'temp',
            '[',
            'apple',
            ']',
            '=',
            'other_class',
            '.',
            'get_stuff',
            '(',
            'true',
            ')',
            ';',
            'do',
            'thing',
            '(',
            'arg',
            ')',
            ';',
            'while',
            '(',
            'true',
            ')',
            '{',
            'let',
            'temp',
            '=',
            'temp',
            '+',
            '1',
            ';',
            '}',
            'if',
            '(',
            'false',
            ')',
            '{',
            'let',
            'a',
            '=',
            'b',
            ';',
            '}',
            'else',
            '{',
            'let',
            'b',
            '=',
            'a',
            ';',
            '}',
            'return',
            'temp',
            ';',
            '}',
            '}'
            ]

    test = get_compiled_output(tokens)
    print(test)

# test()


if __name__ == '__main__':
    import sys
    compile_input(sys.argv[1])
