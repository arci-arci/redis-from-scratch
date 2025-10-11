import os
import sys
sys.path.append(os.path.abspath("./src"))

import unittest
from utility.commands import check_user_input

class TestBlockMarkdown(unittest.TestCase):
    def test_is_a_command(self):
        self.assertFalse(check_user_input("NOT A COMMAND"))

    def test_len_two_args_command(self):
        self.assertFalse(check_user_input("SET one two three"))

    def test_len_one_args_command(self):
        self.assertFalse(check_user_input("GET one two"))

    def test_len_zero_args_command(self):
        self.assertFalse(check_user_input("PING one"))


if __name__ == "__main__":
    unittest.main()