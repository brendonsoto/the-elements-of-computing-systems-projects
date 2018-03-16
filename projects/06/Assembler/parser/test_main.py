import unittest
from .main import parse_input 
from binary_dict import symbols


class TestParser(unittest.TestCase):

    def test_parse_input_comment(self):
        parsedInput = parse_input('// This is a comment', 0)
        self.assertFalse(parsedInput)

    def test_parse_input_A(self):
        parsedInput = parse_input('@1', 1)
        self.assertDictEqual(parsedInput, { 'type': 'A', 'address': 1 })

    def test_parse_input_A_predefined_symbol(self):
        parsedInput = parse_input('@KBD', 2)
        self.assertDictEqual(parsedInput, { 'type': 'A', 'address': 24576 })

    def test_parse_input_A_predefined_symbol_2(self):
        parsedInput = parse_input('@R0', 2)
        self.assertDictEqual(parsedInput, { 'type': 'A', 'address': 0 })

    def test_parse_input_A_user_symbol(self):
        parsedInput = parse_input('@count', 3)
        self.assertDictEqual(parsedInput, { 'type': 'A', 'address': 'count' })

    def test_parse_input_C_comment(self):
        parsedInput = parse_input('M=D     // A comment', 4)
        self.assertDictEqual(parsedInput, { 'type': 'C', 'comp': 'D', 'dest': 'M', 'jump': 'null' })

    def test_parse_input_C_no_jump(self):
        parsedInput = parse_input('M=1', 4)
        self.assertDictEqual(parsedInput, { 'type': 'C', 'comp': '1', 'dest': 'M', 'jump': 'null' })

    def test_parse_input_C_jump(self):
        parsedInput = parse_input('D;JGT', 5)
        self.assertDictEqual(parsedInput, { 'type': 'C', 'comp': 'D', 'dest': 'null', 'jump': 'JGT' })

    def test_parse_input_location(self):
        expected = symbols.table.copy()
        expected['LOOP'] = 6
        parsedInput = parse_input('(LOOP)', 6)
        self.assertFalse(parsedInput)
        self.assertDictEqual(symbols.table, expected)

if __name__ == '__main__':
    unittest.main()
