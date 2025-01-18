import asyncio
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from OracleBot import OracleBot
from InsultBot import InsultBot
from BotManager import BotManager

class TestOracleBot(unittest.TestCase):

    @patch('mcpi.minecraft.Minecraft.create')  
    @patch('mcpi.minecraft.Minecraft.postToChat') 
    def setUp(self, mock_post_to_chat, mock_minecraft_create):
        self.mock_mc = MagicMock()
        mock_minecraft_create.return_value = self.mock_mc

        self.oracle_bot = OracleBot(self.mock_mc)
        self.insult_bot = InsultBot(self.mock_mc)
        self.bot_manager = BotManager(self.mock_mc)
        self.bot_manager.add_agent("insult", self.insult_bot)
        self.bot_manager.add_agent("oracle", self.oracle_bot)

    def tearDown(self):
        self.mock_mc.reset_mock()
        del self.oracle_bot
        del self.insult_bot
        del self.mock_mc

    # Test 1: Verify that get_response returns the correct response
    def test_get_response_valid_question(self):
        question = "How do I move in Minecraft?"
        expected_response = "Use the W, A, S, and D keys to move, and the spacebar to jump."
        actual_response = self.oracle_bot.get_response(question)
        self.assertEqual(expected_response, actual_response)

    def test_get_response_unknown_question(self):
        question = "How do I fly?"
        expected_response = "Sorry, I don't know the answer to that question."
        actual_response = self.oracle_bot.get_response(question)
        self.assertEqual(expected_response, actual_response)

    # Test 2: Verify that show_available_questions displays the correct questions
    def test_show_available_questions(self):
        self.oracle_bot.show_available_questions()

        self.mock_mc.postToChat.assert_any_call("OracleBot: You can ask the following questions:")
        self.mock_mc.postToChat.assert_any_call("- how do i move in minecraft")
        self.mock_mc.postToChat.assert_any_call("- how do i open my inventory")
        self.mock_mc.postToChat.assert_any_call("- how do i break blocks")
        self.mock_mc.postToChat.assert_any_call("- how do i place blocks")


if __name__ == "__main__":
    unittest.main()
