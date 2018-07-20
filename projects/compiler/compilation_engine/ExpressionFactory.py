from TokenIterator import TokenIterator


unary_operators = '-', '~'
operators = unary_operators + ('+', '-', '*', '/', '&', '|', '<', '>', '=')
keywords = 'true', 'false', 'null', 'this'


'''
get_expression
input: a list of tokens
output: a dictionary representing an expression
'''
def get_expression(tokens):
    token_iterator = TokenIterator(tokens)

    # Let's assume the currenttoken is at the term
    term = token_iterator.getCurrentToken()
    expression = { 'node_type': 'expression', }

    # Integer constant
    if term.isdigit():
        expression['expression_type'] = 'integer'
        expression['value'] = term

    # Keyword constant
    elif term in keywords:
        expression['expression_type'] = 'keyword'
        expression['value'] = term

    # String constant -- (str) is used to determine string constants
    elif '(str)' in term:
        expression['expression_type'] = 'string'
        expression['value'] = term.replace('(str) ', '')

    # Unary
    elif term in unary_operators:
        expression = get_unary_expression(token_iterator)

    # Expression in parenthesis -- i.e. (5 - 4)
    elif term is '(':
        expression_tokens = get_inner_expression(token_iterator, ')')
        expression['expression_type'] = 'parenthetical'
        expression['expressions'] = get_expression(expression_tokens)

    # Otherwise we either have an array accessor or a subroutine call
    if token_iterator.isThereNextToken():

        # First get next token for reference
        next_token = token_iterator.getNextToken()

        if next_token is '[':
            expression_tokens = get_inner_expression(token_iterator, ']')
            expression['expression_type'] = 'array_accessor'
            expression['array'] = term
            expression['accessor'] = get_expression(expression_tokens)

        elif next_token is '(':
            expression_tokens = get_inner_expression(token_iterator, ')')
            expression['expression_type'] = 'subroutine_call'
            expression['name'] = term
            expression['expression_list'] = get_expression(expression_tokens)

        elif next_token is '.':
            expression_tokens = get_inner_expression(token_iterator, ')')
            expression['expression_type'] = 'subroutine_parent'
            expression['class'] = term
            expression['expression_list'] = get_expression(expression_tokens)

        # TODO Check this out -- see if it's viable for multiple operations
        elif next_token in operators:
            expression['operator'] = next_token
            expression_tokens = get_remainder_of_expression(token_iterator)
            expression['operated_value'] = get_expression(expression_tokens)

        else:
            raise ValueError("Expected a [/(/operator but received {0}".format(next_token))

    elif not token_iterator.isThereNextToken() and not 'value' in expression.keys():
        expression['term_type'] = 'varName'
        expression['value'] = term

    return expression


def get_unary_expression(token_iterator):
    term = token_iterator.getCurrentToken()

    # A unary operation contains an expression, so we'll have to grab everything after the unary operator to get the sub expression
    expression_tokens = []
    while token_iterator.currentIndex != len(token_iterator.tokens) - 1:
        expression_tokens.append(token_iterator.getNextToken())

    return {
            'node_type': 'expression',
            'expression_type': 'unary',
            'unary_operator': term,
            'value': get_expression(expression_tokens)
            }


def get_remainder_of_expression(token_iterator):
    expression_tokens = []

    while token_iterator.isThereNextToken():
        expression_tokens.append(token_iterator.getNextToken())

    return expression_tokens

def get_inner_expression(token_iterator, ending_char):
    starting_char = token_iterator.getCurrentToken()
    indentation_level = 0
    expression_tokens = []

    while token_iterator.isThereNextToken():
        token = token_iterator.getNextToken()

        if token is starting_char:
            indentation_level += 1

        if token is ending_char and indentation_level > 0:
            indentation_level -= 1

        elif token is ending_char:
            break

        expression_tokens.append(token)

    return expression_tokens
