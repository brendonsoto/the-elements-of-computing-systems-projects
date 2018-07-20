from SubroutineBody import get_subroutine_body


def set_subroutine_decs(token_iterator):
    subroutine = {
            'subroutine_type': token_iterator.getCurrentToken(),
            'return_type': token_iterator.getNextToken(),
            'name': token_iterator.getNextToken(),
            'parameters': []
            }

    if token_iterator.getNextToken() != '(':
        raise ValueError("Expected '(' after function declaration {0}".format(subroutine['name']))

    # At this point we're at the beginning of the parameter list, (, so let's get the parameters
    # Parameters are listed as: type + varName | so use tuples to represent that
    while token_iterator.getNextToken() != ')':
        if token_iterator.getCurrentToken() != ',':
            parameter = token_iterator.getCurrentToken(), token_iterator.getNextToken()
            subroutine['parameters'].append(parameter)

    # Now set the subroutine body
    subroutine['body'] = get_subroutine_body(token_iterator)

    # Save the dictionary to the object
    return subroutine

def get_subroutine_decs(token_iterator):
    valid_subroutine_types = 'constructor', 'function', 'method'
    subroutines = []

    while token_iterator.getCurrentToken() in valid_subroutine_types:
        subroutines.append(set_subroutine_decs(token_iterator)) # Don't need to go to the next token because set_subroutine_decs will increment it as a side effect

    return {
            'node_type': 'program_structure',
            'program_structure': 'subroutine_dec',
            'subroutines': subroutines
            }
