import unittest
import asyncio
from unittest.mock import MagicMock, patch
import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MinecraftAgent import MinecraftAgent 
from OpenAI import OpenAIBot 

class TestOpenAIBot(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.env_patcher = patch.dict(
            os.environ, {"OPENAI_API_KEY": "test_key"}, clear=True
        )
        self.env_patcher.start()
        self.mc_mock = MagicMock()

    def tearDown(self):
        self.env_patcher.stop()

    # Test 1
    def test_initialization_with_api_key(self):
        bot = OpenAIBot(self.mc_mock)
        self.assertEqual(bot.name, "OpenAIBot")
        self.assertIsNotNone(bot.client, "OpenAI client should be initialized.")

    # Test 2
    @patch("OpenAI.OpenAI")  
    async def test_get_response_success(self, mock_openai_class):
        bot = OpenAIBot(self.mc_mock)

        mock_client_instance = mock_openai_class.return_value
        mock_chat = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices = [
            MagicMock(message=MagicMock(content="Test response"))
        ]
        mock_chat.completions.create.return_value = mock_completion
        mock_client_instance.chat = mock_chat

        response = await bot.get_response("Hello Bot")
        self.assertEqual(response, "Test response")
        mock_chat.completions.create.assert_called_once()

    # Test 3
    @patch("OpenAI.OpenAI")  
    async def test_get_response_exception(self, mock_openai_class):
        bot = OpenAIBot(self.mc_mock)

        mock_client_instance = mock_openai_class.return_value
        mock_chat = MagicMock()
        mock_chat.completions.create.side_effect = Exception("Mocked error")
        mock_client_instance.chat = mock_chat

        response = await bot.get_response("Any prompt")
        self.assertIn("Error generating response: Mocked error", response)

    # Test 4
    async def test_perform_task_normal_execution(self):
        bot = OpenAIBot(self.mc_mock)

        bot.send_message = MagicMock()

        stop_event = asyncio.Event()
        task = asyncio.create_task(bot.perform_task(stop_event))

        await asyncio.sleep(0.1)

        stop_event.set()
        await task

        expected_messages = [
            unittest.mock.call("Ready to respond questions."),
            unittest.mock.call("OpenAIBot desactivated.")
        ]
        bot.send_message.assert_has_calls(expected_messages)

    # Test 5
    async def test_perform_task_interrupted_early(self):
        bot = OpenAIBot(self.mc_mock)
        bot.send_message = MagicMock()

        stop_event = asyncio.Event()
        task = asyncio.create_task(bot.perform_task(stop_event))

        stop_event.set()
        await task

        expected_messages = [
            unittest.mock.call("Ready to respond questions."),
            unittest.mock.call("OpenAIBot desactivated.")
        ]
        bot.send_message.assert_has_calls(expected_messages)

if __name__ == "__main__":
    unittest.main()