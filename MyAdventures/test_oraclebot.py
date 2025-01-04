import unittest
from unittest.mock import patch, MagicMock
from OracleBot import OracleBot
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestOracleBot(unittest.TestCase):
    @patch('mcpi.minecraft.Minecraft.create')
    @patch('mcpi.minecraft.Minecraft.postToChat')
    def setUp(self, mock_post_to_chat, mock_minecraft_create):
        self.mock_mc = MagicMock()
        mock_minecraft_create.return_value = self.mock_mc

        self.oracle_bot = OracleBot(self.mock_mc)

    def tearDown(self):
        self.mock_mc.reset_mock()
        del self.oracle_bot
        del self.mock_mc

    def test_get_response_valid_question(self):
        ...

    def test_get_response_unknown_question(self):
        ...

    def test_show_available_questions(self):
        ...

if __name__ == "__main__":
    unittest.main()