import unittest
import symbols


expected = symbols.table.copy()
class TestSymbolTable(unittest.TestCase):

    def test_add_entries_from_file(self):
        expected['INFINITE_LOOP'] = 23
        expected['LOOP'] = 10
        symbols.add_entries_from_file('../rect/Rect.asm')
        self.assertDictEqual(symbols.table, expected)

    def test_add_entries_from_file_fail(self):
        self.assertRaises(ValueError, symbols.add_entries_from_file, '../../rect/Rect.hack')

    def test_add_new_entry(self):
        expected['_address'] = 17
        expected['test'] = 16
        symbols.add_entry('test')
        self.assertDictEqual(symbols.table, expected)

    # Seems like tests run alphabetically...
    def test_add_new_entry_location(self):
        expected['MOOP'] = 6
        symbols.add_entry({ 'MOOP': 6 })
        self.assertDictEqual(symbols.table, expected)


if __name__ == '__main__':
    unittest.main()
