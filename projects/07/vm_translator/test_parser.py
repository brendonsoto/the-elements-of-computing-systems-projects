import unittest
import parser


class TestParser(unittest.TestCase):
    def test_read_file(self):
        expected = [
                'push constant 7',
                'push constant 8',
                'add'
                ]
        lines = parser.read_file('../StackArithmetic/SimpleAdd/SimpleAdd.vm')
        self.assertListEqual(lines, expected)

    def test_parse_instructions(self):
        lines = parser.read_file('../StackArithmetic/SimpleAdd/SimpleAdd.vm')
        expected = [
                { 'type': 'push', 'value': { 'type': 'constant', 'value': 7 } },
                { 'type': 'push', 'value': { 'type': 'constant', 'value': 8 } },
                { 'type': 'arithmetic', 'value': 'add' }
                ]
        instructions = parser.get_instructions(lines)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestParser('test_read_file'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
