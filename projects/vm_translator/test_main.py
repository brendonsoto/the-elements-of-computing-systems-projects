import unittest
import main as vm_translator


class TestMain(unittest.TestCase):
    def test_check_if_helpers_are_needed(self):
        are_helpers_needed = vm_translator.check_if_helpers_are_needed('../08/FunctionCalls/FibonacciElement/Main.vm')
        self.assertTrue(are_helpers_needed)

    def test_check_if_directory_needs_helpers(self):
        import os

        # Setup stuff
        directory_path = '../08/FunctionCalls/FibonacciElement'
        os.chdir(directory_path)

        # The test
        are_helpers_needed = vm_translator.check_if_directory_needs_helpers('./')
        self.assertTrue(are_helpers_needed)

        # Breakdown
        os.chdir('../../../vm_translator')
