# tests/test_tnt_bot.py
import unittest
from unittest.mock import Mock, MagicMock, patch, call
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from TNTbot import TNTBot

class TestTNTBot(unittest.TestCase):
    def setUp(self):
        # Mocck minecraft instance
        self.mock_mc = Mock()
         # Instance of TNTBot
        self.tnt_bot = TNTBot(self.mock_mc)

    #Test 1: Verify that the TNTBot sends the message "Boom!" when performing the task
    @patch('TNTbot.time.sleep', return_value=None)  
    def test_perform_task_normal_execution(self, mock_sleep):
        mock_position = Mock(x=50, y=70, z=50)
        self.mock_mc.player.getTilePos.return_value = mock_position

        self.tnt_bot.send_message = MagicMock()

        stop_event = threading.Event()
        thread = threading.Thread(target=self.tnt_bot.perform_task, args=(stop_event,))
        thread.start()

        thread.join(timeout=2)  

        stop_event.set()
        thread.join()

        self.tnt_bot.send_message.assert_called_once_with("Boom!")
    
    #Test 2: Verify that the TNTBot sends the message "TNT task interrupted." when the task is interrupted
    @patch('TNTbot.time.sleep', return_value=None) 
    def test_perform_task_with_exception(self, mock_sleep):
        self.mock_mc.player.getTilePos.side_effect = Exception("Test exception")
        self.tnt_bot.send_message = MagicMock()

        stop_event = threading.Event()
        self.tnt_bot.perform_task(stop_event)

        self.tnt_bot.send_message.assert_called_once_with("Error getting player position: Test exception")

if __name__ == "__main__":
    unittest.main()