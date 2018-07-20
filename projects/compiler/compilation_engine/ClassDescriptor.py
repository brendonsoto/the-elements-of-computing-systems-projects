from ClassVarDecs import get_class_var_decs
from SubroutineDecs import get_subroutine_decs


def get_class_vars(token_iterator):

    # At this point token_iterator is at '{' so we need to go to the next token before getting the varDecs
    token_iterator.next()
    return get_class_var_decs(token_iterator)
    # The above function moves the token_iterator index to the subroutine (if there is one)

def get_class_description(token_iterator):
    if token_iterator.getCurrentToken() != 'class':
        raise ValueError('Given token is not "class"')

    name = token_iterator.getNextToken()

    if token_iterator.getNextToken() != '{':
        raise ValueError("Expected '{{' at beginning of class {0} declaration".format(name))

    classVars = get_class_vars(token_iterator)
    subroutines = get_subroutine_decs(token_iterator)

    # Check for ending }
    if token_iterator.getCurrentToken() != '}':
        raise ValueError("Expected '}}' at end of class {0} declaration".format(name))

    return {
            'node_type': 'program_structure',
            'program_structure': 'class',
            'name': name,
            'varDecs': classVars,
            'subroutines': subroutines
            }
