from ExpressionFactory import get_expression


def get_return_statement(token_iterator):
    expression = None
    expression_tokens = []

    while token_iterator.getNextToken() != ';':
        expression_tokens.append(token_iterator.getCurrentToken())

    if len(expression_tokens) > 0:
        expression = get_expression(expression_tokens)

    return {
            'node_type': 'statement',
            'statement_type': 'return',
            'expression': expression
            }
