import unittest
import code_writer


class TestCodeWriter(unittest.TestCase):
    def test_push_constant(self):
        expected = "@7\nD=A\n@SP\nA=M\nM=D\n@SP\nAM=M+1\n"
        assembly_code = code_writer.write_push({ 'type': 'constant', 'value': 7 })
        self.assertEqual(assembly_code, expected)

    def test_create_code(self):
        expected = "@7\nD=A\n@SP\nA=M\nM=D\n@SP\nAM=M+1\n@8\nD=A\n@SP\nA=M\nM=D\n@SP\nAM=M+1\n@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n"
        vm_instructions = [
                {'type': 'push', 'value': {'type': 'constant', 'value': '7'}},
                {'type': 'push', 'value': {'type': 'constant', 'value': '8'}},
                {'type': 'arithmetic', 'value': 'add'}
                ]
        assembly_code = code_writer.create_code(vm_instructions)
        self.assertEqual(assembly_code, expected)
