import unittest
from unittest.mock import patch, MagicMock
from OracleBot import OracleBot
import time
import os
import sys

# Añadir el directorio raíz del proyecto al path para que Python pueda encontrar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestOracleBot(unittest.TestCase):

    @patch('mcpi.minecraft.Minecraft.create')  # Mockear la creación de Minecraft
    @patch('mcpi.minecraft.Minecraft.postToChat')  # Mockear el método postToChat
    def setUp(self, mock_post_to_chat, mock_minecraft_create):
        # Mockear la instancia de Minecraft
        self.mock_mc = MagicMock()
        mock_minecraft_create.return_value = self.mock_mc

        # Instanciar el OracleBot con el mock_mc
        self.oracle_bot = OracleBot(self.mock_mc)

    def tearDown(self):
        # Ensure that all mock objects are properly cleaned up
        self.mock_mc.reset_mock()
        del self.oracle_bot
        del self.mock_mc

    # Test 1: Verify that get_response returns the correct response
    def test_get_response_valid_question(self):
        question = "How do I move in Minecraft?"
        expected_response = "Use the W, A, S, and D keys to move, and the spacebar to jump."
        actual_response = self.oracle_bot.get_response(question)
        self.assertEqual(expected_response, actual_response)

    def test_get_response_unknown_question(self):
        question = "What is the meaning of life?"
        expected_response = "Sorry, I don't know the answer to that question."
        actual_response = self.oracle_bot.get_response(question)
        self.assertEqual(expected_response, actual_response)

    # Test 2: Verify that show_available_questions displays the correct questions
    def test_show_available_questions(self):
        # Simulate the bot showing available questions
        self.oracle_bot.show_available_questions()

        # Verify that the correct questions were posted to chat
        self.mock_mc.postToChat.assert_any_call("OracleBot: You can ask the following questions:")
        self.mock_mc.postToChat.assert_any_call("- How do I move in Minecraft?")
        self.mock_mc.postToChat.assert_any_call("- How do I open my inventory?")
        self.mock_mc.postToChat.assert_any_call("- How do I break blocks?")
        self.mock_mc.postToChat.assert_any_call("- How do I place blocks?")


if __name__ == "__main__":
    unittest.main()