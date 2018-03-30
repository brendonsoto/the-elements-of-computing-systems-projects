import unittest
import parser


class TestParser(unittest.TestCase):
    def test_get_vm_code_from_file(self):
        expected = [
                'push constant 7',
                'push constant 8',
                'add'
                ]
        lines = parser.get_vm_code_from_file('../../completed-projects/07/StackArithmetic/SimpleAdd/SimpleAdd.vm')
        self.assertListEqual(lines, expected)

    def test_parse_instructions(self):
        lines = parser.get_vm_code_from_file('../../completed-projects/07/StackArithmetic/SimpleAdd/SimpleAdd.vm')
        expected = [
                { 'type': 'push', 'value': { 'type': 'constant', 'value': 7 } },
                { 'type': 'push', 'value': { 'type': 'constant', 'value': 8 } },
                { 'type': 'arithmetic', 'value': 'add' }
                ]
        instructions = parser.get_instructions(lines)

    def test_translate_pop(self):
        line = 'pop argument 1'
        expected = { 'type': 'pop', 'value': { 'base': 'argument', 'index': '1' } }
        translation = parser.get_parsed_command(line)
        self.assertDictEqual(translation, expected)

    def test_remove_inline_comments(self):
        line = 'lt      // This is a test comment'
        expected = 'lt'
        line_without_comments = parser.remove_inline_comments(line)
        self.assertEqual(line_without_comments, expected)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestParser('test_get_vm_code_from_file'))
    suite.addTest(TestParser('test_remove_inline_comments'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
