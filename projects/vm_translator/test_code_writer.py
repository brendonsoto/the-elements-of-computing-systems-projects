import unittest
import code_writer


class TestCodeWriter(unittest.TestCase):
    def test_pop(self):
        expected = "@LCL\nD=M\n@2\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
        assembly_code = code_writer.write_pop({ 'base': 'local', 'index': 2 })
        self.assertEqual(assembly_code, expected)

    def test_push_constant(self):
        instruction = { 'type': 'constant', 'value': 7 }
        expected = "@7\nD=A\n@SP\nA=M\nM=D\n@SP\nAM=M+1\n"
        assembly_code = code_writer.write_push(instruction)
        self.assertEqual(assembly_code, expected)

    def test_push_vm_symbol_local_0(self):
        instruction = { 'type': 'local', 'value': '0' }
        expected = "@LCL\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        assembly_code = code_writer.write_push(instruction)
        self.assertEqual(assembly_code, expected)

    def test_push_vm_symbol_temp_2(self):
        instruction = { 'type': 'temp', 'value': '2' }
        expected = "@R7\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        assembly_code = code_writer.write_push(instruction)
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
