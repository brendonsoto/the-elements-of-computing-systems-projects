from StatementFactory import StatementFactory


def get_local_varDecs(token_iterator):
    var_type = token_iterator.getNextToken()
    variables = []

    while token_iterator.getNextToken() != ';':
        if token_iterator.getCurrentToken() != ',':
            variables.append(token_iterator.getCurrentToken())

    return {
            'node_type': 'program_structure',
            'program_structure': 'varDec',
            'type': var_type,
            'vars': variables
            }


def get_subroutine_body(token_iterator):
    variables = []
    statements = []

    if token_iterator.getNextToken() != '{':
        raise ValueError("Expected '{{' at beginning of class {0} declaration".format(className))

    next_token = token_iterator.getNextToken()

    # Get varDecs
    while next_token is 'var':
        variables = get_local_varDecs(token_iterator)
        next_token = token_iterator.getNextToken()

    # Get statements
    while next_token != '}':
        statements.append(StatementFactory(token_iterator))
        next_token = token_iterator.getNextToken()

    # Check for ending }
    if token_iterator.getCurrentToken() != '}':
        raise ValueError("Expected '}}' at end of class {0} declaration".format(className))

    return {
            'node_type': 'program_structure',
            'program_structure': 'subroutine_body',
            'variables': variables,
            'statements': statements
            }
