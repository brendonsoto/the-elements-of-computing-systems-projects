# NOTE - Oops, I've been doing the docstrings wrong this entire time. They go under the func.

DEFAULT_INDENTATION = ' ' * 2
# TODO  -- Make a shortcut function for keyword + id tag combos?


'''
convert_class
Input: dict
{'node_type': 'program_structure', 'program_structure': 'class', 'name': 'Main', 'varDecs': [], 'subroutines': []}
Output: XML
<class>
  <keyword> class </keyword>
  <identifier> Main </identifier>
  <symbol> { </symbol>
  <classVarDec>
    ...
  </classVarDec>
  <subroutineDec>
      ...
  </subroutineDec>
</class>
'''
def convert_class(class_dict):
    class_var_dec_tags = ''.join(map(convert_class_var_dec, class_dict['varDecs']))
    # FIXME -- double subroutines is ugly
    subroutine_dec_tags = ''.join(map(convert_subroutine_dec, class_dict['subroutines']['subroutines']))

    xml_tags = [
            "<class>\n",
            "{0}<keyword> {1} </keyword>\n".format(DEFAULT_INDENTATION, class_dict['program_structure']),
            "{0}<identifier> {1} </identifier>\n".format(DEFAULT_INDENTATION, class_dict['name']),
            "{0}<symbol> {{ </symbol>\n".format(DEFAULT_INDENTATION),
            class_var_dec_tags,
            subroutine_dec_tags,
            "{0}<symbol> }} </symbol>\n".format(DEFAULT_INDENTATION),
            "</class>\n"
            ]

    return ''.join(xml_tags)


'''
convert_class_var_dec
Input: Dictionary
{'scope': 'field', 'type': 'int', 'variables': ['count', 'current']},
Output: XML
<classVarDec>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier> count </identifier>
    <symbol> , </symbol>
    <identifier> current </identifier>
    <symbol> ; </symbol>
</classVarDec>
'''
def convert_class_var_dec(class_var_dec_dict):
    indentation_level = 2 # 1 because it's the first indentation 
    var_decs_indentation = DEFAULT_INDENTATION * indentation_level

    identifier_tags = [
            "{0}<identifier> {1} </identifier>\n".format(var_decs_indentation, class_var_dec_dict['variables'][0])
            ]

    for variable in class_var_dec_dict['variables'][1:]:
        identifier_tags.extend([
            "{0}<symbol> , </symbol>\n".format(var_decs_indentation),
            "{0}<identifier> {1} </identifier>\n".format(var_decs_indentation, variable)
            ])

    xml_tags = [
            "{0}<classVarDec>\n".format(DEFAULT_INDENTATION),
            "{0}<keyword> {1} </keyword>\n".format(var_decs_indentation, class_var_dec_dict['scope']),
            "{0}<keyword> {1} </keyword>\n".format(var_decs_indentation, class_var_dec_dict['type']),
            ''.join(identifier_tags),
            "{0}<symbol> ; </symbol>\n".format(var_decs_indentation),
            "{0}</classVarDec>\n".format(DEFAULT_INDENTATION)
            ]

    return ''.join(xml_tags)


# NOTE Input from this one is nested in another dictionary
'''
convert_subroutine_dec
Input: Dictionary
{'subroutine_type': 'function', 'return_type': 'void', 'name': 'main', 'parameters': [''], 'body': {...}}
parameters is a list of type + identifiers: [int count, boolean isTrue, char firstLetter, className class]
Output: XML Shell
<subroutineDec>
    <keyword> function </keyword>
    <keyword> void </keyword>
    <identifier> main </identifier>
    <symbol> ( </symbol>
    <parameterList>
      <keyword> int </keyword>
      <identifier> Ax </identifier>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
        ...
    </subroutineBody>
</subroutineDec>
'''
def convert_subroutine_dec(subroutine_dec_dict):

    # Determine the indentation 
    indentation_level = 2 # 1 because it's the first indentation 
    base_indentation = DEFAULT_INDENTATION * indentation_level
    inner_subroutine_indentation = base_indentation + DEFAULT_INDENTATION
    param_list_indentation = inner_subroutine_indentation + DEFAULT_INDENTATION

    # The XML Tags
    xml_tags = [
            "{0}<subroutineDec>\n".format(base_indentation),
            "{0}<keyword> {1} </keyword>\n".format(inner_subroutine_indentation, subroutine_dec_dict['subroutine_type']),
            "{0}<keyword> {1} </keyword>\n".format(inner_subroutine_indentation, subroutine_dec_dict['return_type']),
            "{0}<identifier> {1} </identifier>\n".format(inner_subroutine_indentation, subroutine_dec_dict['name']),
            "{0}<symbol> ( </symbol>\n".format(inner_subroutine_indentation),
            convert_param_list(subroutine_dec_dict['parameters'], inner_subroutine_indentation),
            "{0}<symbol> ) </symbol>\n".format(inner_subroutine_indentation),
            convert_subroutine_body(subroutine_dec_dict['body'], inner_subroutine_indentation),
            "{0}</subroutineDec>\n".format(base_indentation)
            ]

    return ''.join(xml_tags)

'''
convert_param_list
Input: list of tuples
[(int, count), (boolean, isTrue)]
Output: XML
<parameterList>
      <keyword> int </keyword>
      <identifier> count </identifier>
      <symbol> , </symbol>
      <keyword> boolean </keyword>
      <identifier> isTrue </identifier>
</parameterList>
'''
def convert_param_list(param_list, prev_indentation_level):

    # Determine the indentation 
    base_indentation = prev_indentation_level + DEFAULT_INDENTATION
    parameter_indentation = base_indentation + DEFAULT_INDENTATION

    # XML Tags
    parameter_tags = [
            "{0}<keyword> {1} </keyword>\n".format(parameter_indentation, param_list[0][0]),
            "{0}<identifier> {1} </identifier>\n".format(parameter_indentation, param_list[0][1])
            ]

    for param_tuple in param_list[1:]:
        parameter_tags.extend([
            "{0}<symbol> , </symbol>\n".format(parameter_indentation),
            "{0}<keyword> {1} </keyword>\n".format(parameter_indentation, param_tuple[0]),
            "{0}<identifier> {1} </identifier>\n".format(parameter_indentation, param_tuple[1])
            ])

    xml_tags = [
            "{0}<parameterList>\n".format(base_indentation),
            ''.join(parameter_tags),
            "{0}</parameterList>\n".format(base_indentation)
            ]

    return ''.join(xml_tags)


'''
convert_subroutine_body
Input: dict
{'node_type': 'program_structure', 'program_structure': 'subroutine_body', 'variables': {}, 'statements': []
Output: XML
<subroutineBody>
    <symbol>
        <varDec>
            ...
        </varDec>
        <statements>
            ...
        </statements>
    </symbol>
</subroutineBody>
'''
def convert_subroutine_body(body_dict, prev_indentation_level):
    indentation_level = prev_indentation_level + DEFAULT_INDENTATION
    symbol_indentation = indentation_level + DEFAULT_INDENTATION
    main_indentation = symbol_indentation + DEFAULT_INDENTATION

    xml_tags = [
            "{0}<subroutineBody>\n".format(indentation_level),
            "{0}<symbol> {{ </symbol>\n".format(symbol_indentation),
            convert_subroutine_var_decs(body_dict['variables'], main_indentation),
            # statements
            "{0}<symbol> }} </symbol>\n".format(symbol_indentation),
            "{0}</subroutineBody>\n".format(indentation_level)
            ]

    return ''.join(xml_tags)


def convert_subroutine_var_decs(var_decs, prev_indentation_level):
    var_decs_indentation = prev_indentation_level + DEFAULT_INDENTATION

    identifier_tags = [
            "{0}<identifier> {1} </identifier>\n".format(var_decs_indentation, var_decs['vars'][0])
            ]

    for variable in var_decs['vars'][1:]:
        identifier_tags.extend([
            "{0}<symbol> , </symbol>\n".format(var_decs_indentation),
            "{0}<identifier> {1} </identifier>\n".format(var_decs_indentation, variable)
            ])

    xml_tags = [
            "{0}<varDec>\n".format(prev_indentation_level),
            "{0}<keyword> var </keyword>\n".format(var_decs_indentation),
            ''.join(identifier_tags),
            "{0}<symbol> ; </symbol>\n".format(var_decs_indentation),
            "{0}</varDec>\n".format(prev_indentation_level)
            ]

    return ''.join(xml_tags)




'''
convert_expression
Input: dict
{'node_type': 'expression', 'expression_type': 'integer', 'value': '1'}
Output: XML
<expression>
  <term>
    <integerConstant> 1 </integerConstant>
  </term>
</expression>
'''
def convert_expression(expression_dict, indentation_level):
    expression_indentation = DEFAULT_INDENTATION * indentation_level
    term_indentation = expression_indentation + ' ' * 2

    xml_tags = [
            "{0}<expression>\n".format(expression_indentation),
            "{0}<term>\n".format(term_indentation),
            get_term(expression_dict['value'], term_indentation),
            "{0}</term>\n".format(term_indentation),
            "{0}</expression>\n".format(expression_indentation),
            ]

    return ''.join(xml_tags)


def get_term(value, indentation_level):
    value_indentation = indentation_level + DEFAULT_INDENTATION
    # Integer constant
    if value.isdigit():
        return "{0}<integerConstant> {1} </integerConstant>\n".format(value_indentation, value)


# print(convert_expression({'node_type': 'expression', 'expression_type': 'integer', 'value': '1'}, 0))
# print(convert_expression({'node_type': 'expression', 'expression_type': 'keyword', 'value': 'true'}, 0))
# print(convert_expression({'node_type': 'expression', 'expression_type': 'integer', 'string': '(str)string constant'}, 0))
