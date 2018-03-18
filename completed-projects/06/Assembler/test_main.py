import unittest
import main as assembler
import parser.main as parser


class TestAssembler(unittest.TestCase):
    def test_synthesize_A_instruction(self):
        instruction = assembler.synthesize_A_instruction({ 'type': 'A', 'address': 1 })
        self.assertEqual(instruction, "{0:016b}\n".format(1))

    def test_synthesize_A_instruction_predefined_symbol(self):
        instruction = assembler.synthesize_A_instruction({ 'type': 'A', 'address': 'SCREEN' })
        self.assertEqual(instruction, "{0:016b}\n".format(16384))

    def test_synthesize_A_instruction_user_symbol(self):
        parser.parse_input('@i', 7)
        instruction = assembler.synthesize_A_instruction({ 'type': 'A', 'address': 'i' })
        self.assertEqual(instruction, "{0:016b}\n".format(16))

    def test_synthesizing_C_instruction(self):
        instruction = assembler.synthesize_C_instruction({ 'type': 'C', 'comp': 'M+1', 'dest': 'M', 'jump': 'null' })
        self.assertEqual(instruction, '1111110111001000\n')


if __name__ == '__main__':
    unittest.main()
