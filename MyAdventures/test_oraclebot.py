import unittest
from unittest.mock import MagicMock
from OracleBot import OracleBot

class TestOracleBot(unittest.TestCase):

    def setUp(self):
        # Mocking the Minecraft Agent (mc)
        self.mock_mc = MagicMock()
        
        # Instantiating the OracleBot with the mock_mc
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
