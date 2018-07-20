# This is a pretty terrible way of doing this hahah
# TODO Reflect & write -- why is this a terrible approach?
# Initial reflection - because we're kind of shoe-horning functions into classes here
# It would've been better to have functions that return data structures representing the declarations/token bits
# My main problem is, what would the structure be and how would we output it?
# I think it would simply be dictionaries and having a separate output function for each
# Let's save reflections for once the entire thing is done though

def get_decs(token_iterator):
    variables = []
    scope = token_iterator.getCurrentToken()
    var_type = token_iterator.getNextToken()

    while token_iterator.getNextToken() != ';':
        if token_iterator.getCurrentToken() != ',':
            variables.append(token_iterator.getCurrentToken())

    return {
            'scope': scope,
            'type': var_type,
            'variables': variables
            }

def get_class_var_decs(token_iterator):
    declarations = []
    valid_scopes = 'static', 'field'

    # if token_iterator.getCurrentToken() in valid_scopes:
    while token_iterator.getCurrentToken() in valid_scopes:
        declarations.append(get_decs(token_iterator))
        token_iterator.next() # At this point, we're at ';' so go to the next

    return declarations 
