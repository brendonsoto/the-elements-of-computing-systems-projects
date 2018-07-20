from ExpressionFactory import get_expression


def get_do_statement(token_iterator):
    subroutine_call_tokens = []

    while token_iterator.getNextToken() != ';':
        subroutine_call_tokens.append(token_iterator.getCurrentToken())

    return {
            'node_type': 'statement',
            'statement_type': 'do',
            'subroutine': get_expression(subroutine_call_tokens)
            }
