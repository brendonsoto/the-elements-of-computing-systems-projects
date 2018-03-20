import unittest
import code_writer


# NOTE -- Midway writing this (test neg) and I'm wondering if these tests are worth it
# They are simply testing for strings.
class TestCodeWriter(unittest.TestCase):
    def test_arithmetic_add(self):
        expected = "@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n"
        assembly_code = code_writer.write_arithmetic('add') 
        self.assertEqual(assembly_code, expected)

    def test_arithmetic_sub(self):
        expected = "@SP\nAM=M-1\nD=M\nA=A-1\nM=D-M\n"
        assembly_code = code_writer.write_arithmetic('sub') 
        self.assertEqual(assembly_code, expected)

    def test_arithmetic_neg(self):
        expected = "@SP\nA=M-1\nM=-M\n"
        assembly_code = code_writer.write_arithmetic('neg') 
        self.assertEqual(assembly_code, expected)

    def test_arithmetic_eq(self):
        expected = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@0;JMP\n@16\nD;JEQ\nD=A\n@SP\nA=A-1\nM=D\n"
        assembly_code = code_writer.write_arithmetic('eq') 
        self.assertEqual(assembly_code, expected)

    def test_arithmetic_gt(self):
        expected = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@0;JMP\n@16\nD;JGT\nD=A\n@SP\nA=A-1\nM=D\n"
        assembly_code = code_writer.write_arithmetic('gt') 
        self.assertEqual(assembly_code, expected)

    def test_arithmetic_lt(self):
        expected = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@0;JMP\n@16\nD;JLT\nD=A\n@SP\nA=A-1\nM=D\n"
        assembly_code = code_writer.write_arithmetic('lt') 
        self.assertEqual(assembly_code, expected)

    def test_arithmetic_and(self):
        expected = "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\nA=A+1\n"
        assembly_code = code_writer.write_arithmetic('and')
        self.assertEqual(assembly_code, expected)

    def test_arithmetic_or(self):
        expected = "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\nA=A+1\n"
        assembly_code = code_writer.write_arithmetic('or')
        self.assertEqual(assembly_code, expected)

    def test_arithmetic_not(self):
        expected = "@SP\nA=A-1\nM=!M\nA=A+1\n"
        assembly_code = code_writer.write_arithmetic('not')
        self.assertEqual(assembly_code, expected)

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
