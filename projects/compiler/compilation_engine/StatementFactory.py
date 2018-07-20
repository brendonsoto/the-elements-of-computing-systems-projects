from DoStatement import get_do_statement
from LetStatement import get_let_statement
from ReturnStatement import get_return_statement
from ExpressionFactory import get_expression


def StatementFactory(token_iterator):
    statement_type = token_iterator.getCurrentToken()
    statement_obj = None

    if statement_type is 'do':
        return get_do_statement(token_iterator)
    elif statement_type is 'if':
        return get_if_statement(token_iterator, statement_type)
    elif statement_type is 'let':
        return get_let_statement(token_iterator)
    elif statement_type is 'return':
        return get_return_statement(token_iterator)
    elif statement_type is 'while':
        return get_conditional_statement(token_iterator, statement_type)
    else:
        raise ValueError("Incorrect statement type. Expected [do/if/let/return/while] but received {0}".format(statement_type))

    # At this point we're at the end of whatever statement we just processed so go to the next token
    token_iterator.next()



# Can't put this one in a separate module yet because then it we have cyclic imports
# See https://stackoverflow.com/questions/744373/circular-or-cyclic-imports-in-python
def get_conditional_statement(token_iterator, statement_type):
    if token_iterator.getNextToken() != '(':
        raise ValueError("Incorrect conditional statement. Expected ( but received {0}".format(token_iterator.getCurrentToken()))

    expression_tokens = []

    while token_iterator.getNextToken() != ')':
        expression_tokens.append(token_iterator.getCurrentToken())

    # At this point we're at the ) of the while loop, so now to check and process statements
    if token_iterator.getNextToken() != '{':
        raise ValueError("Incorrect conditional statement. Expected { but received {0}".format(token_iterator.getCurrentToken()))

    statements = []

    while token_iterator.getNextToken() != '}':
        statements.append(StatementFactory(token_iterator))


    return {
            'node_type': 'statement',
            'statement_type': statement_type,
            'expression': get_expression(expression_tokens),
            'statements': statements
            }


def get_if_statement(token_iterator, statement_type):
    statement = get_conditional_statement(token_iterator, statement_type)
    statement['else_statements'] = []

    if token_iterator.getNextToken() is 'else':
        if token_iterator.getNextToken() != '{':
            raise ValueError("Incorrect else statement. Expected { but received {0}".format(token_iterator.getCurrentToken()))

        while token_iterator.getNextToken() != '}':
            statement['else_statements'].append(StatementFactory(token_iterator))

    return statement
