from ExpressionFactory import get_expression


def get_let_statement(token_iterator):
    varName = token_iterator.getNextToken()
    next_token = token_iterator.getNextToken()
    accessor = None
    assignment_tokens = []

    if next_token != '[' and next_token != '=':
        raise ValueError(
                "Expected '[' or '=' at token {0}, but received {1}".format(
                    token_iterator.currentIndex,
                    next_token
                    )
                )

    if next_token is '[':
        inner_expression_tokens = []
        while token_iterator.getNextToken() != ']':
            inner_expression_tokens.append(token_iterator.getCurrentToken())

        accessor = get_expression(inner_expression_tokens)
        token_iterator.next()

    elif next_token != '=':
        raise ValueError("Expected '=' but received {0}".format(next_token))

    while token_iterator.getNextToken() != ';':
        assignment_tokens.append(token_iterator.getCurrentToken())


    return {
            'node_type': 'statement',
            'statement_type': 'let',
            'varName': varName,
            'accessor': accessor,
            'value': get_expression(assignment_tokens)
            }
