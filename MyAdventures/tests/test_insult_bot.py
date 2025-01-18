import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from InsultBot import InsultBot

class TestInsultBot(unittest.IsolatedAsyncioTestCase):
    
    # Test 1: Initialization
    def test_initialization(self):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        
        self.assertEqual(bot.name, "InsultBot")
        self.assertIsInstance(bot.insults, list)
        self.assertTrue(len(bot.insults) > 0)

    # Test 2: Insult List
    def test_insult_list(self):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        expected_insults = [
            "Do you even know how to play?",
            "You're slower than a turtle!",
            "You're a total m***",
            "You can't even build a house!",
            "You're acting s***",
            "You really are a c***",
            "You're a disaster!"
        ]
        self.assertTrue(all(insult in expected_insults for insult in bot.insults))

    # Test 3: Insult Sending
    @patch.object(InsultBot, 'send_message')
    async def test_insult_sending(self, mock_send_message):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        stop_event = asyncio.Event()

    # Test 4: Insult Count
    def test_insult_count(self):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        expected_count = 7  # Update this based on the actual number of insults
        self.assertEqual(len(bot.insults), expected_count)


if __name__ == '__main__':
    unittest.main()
