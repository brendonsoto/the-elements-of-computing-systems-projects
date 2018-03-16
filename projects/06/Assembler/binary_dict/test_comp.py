import unittest
import comp

class TestCompCodes(unittest.TestCase):

    def test_throw_if_undefined(self):
        self.assertRaises(ValueError, comp.getCode, 'Q')

    def test_get_A_code(self):
        code = comp.getCode('D+1')
        self.assertEqual(code, '0011111')

    def test_get_M_code(self):
        code = comp.getCode('M+1')
        self.assertEqual(code, '1110111')

if __name__ == '__main__':
    unittest.main()
