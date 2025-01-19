import unittest
from unittest.mock import Mock, MagicMock, patch
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcpi.block import TNT
from mcpi.block import FIRE
from TNTbot import TNTBot

class TestTNTBot(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_mc = Mock()
        self.tnt_bot = TNTBot(self.mock_mc)
        self.tnt_bot.send_message = MagicMock()


    #Test 1 Verify that TNTBot sends the message "Boom!"
    @patch('TNTbot.asyncio.sleep', return_value=None)
    async def test_perform_task_normal_execution(self, mock_sleep):
        mock_position = Mock(x=50, y=70, z=50)
        self.mock_mc.player.getTilePos.return_value = mock_position
        stop_event = asyncio.Event()
        await self.tnt_bot.perform_task(stop_event)
        self.tnt_bot.send_message.assert_called_with("Boom!")
    
    #Test 2: Verify that TNTBot sends the message "Error getting player position: Test exception"
    @patch('TNTbot.asyncio.sleep', return_value=None)
    async def test_perform_task_with_exception(self, mock_sleep):
        self.mock_mc.player.getTilePos.side_effect = Exception("Test exception")
        stop_event = asyncio.Event()
        await self.tnt_bot.perform_task(stop_event)
        self.tnt_bot.send_message.assert_called_with("Error getting player position: Test exception")
    
    #Test 3: Verify that TNTBot sends the message "TNT task interrupted."
    @patch('TNTbot.asyncio.sleep')
    async def test_perform_task_interrupted(self, mock_sleep):
        mock_position = Mock(x=50, y=70, z=50)
        self.mock_mc.player.getTilePos.return_value = mock_position
        stop_event = asyncio.Event()
        
        async def sleep_side_effect(duration):
            if duration == 1:
                return
            elif duration == 15:
                stop_event.set()
                return
        
        mock_sleep.side_effect = sleep_side_effect
        await self.tnt_bot.perform_task(stop_event)
        
        expected_calls = [
            unittest.mock.call("Boom!"),
            unittest.mock.call("TNT task interrupted.")
        ]
        self.tnt_bot.send_message.assert_has_calls(expected_calls, any_order=False)

    # Test 4: Verify we place the tnt at the correct position
    @patch('TNTbot.asyncio.sleep', return_value=None)
    async def test_tnt_placement(self, mock_sleep):
        mock_position = Mock(x=10, y=64, z=10)
        self.mock_mc.player.getTilePos.return_value = mock_position
        stop_event = asyncio.Event()

        await self.tnt_bot.perform_task(stop_event)
        self.mock_mc.setBlock.assert_any_call(mock_position.x, mock_position.y, mock_position.z, TNT, 1)
        
    # Test 5: Verify we place the fire at the correct position
    @patch('TNTbot.asyncio.sleep', return_value=None)
    async def test_fire_placement(self, mock_sleep):
        mock_position = Mock(x=10, y=64, z=10)
        self.mock_mc.player.getTilePos.return_value = mock_position
        stop_event = asyncio.Event()

        await self.tnt_bot.perform_task(stop_event)
        self.mock_mc.setBlock.assert_any_call(mock_position.x, mock_position.y, mock_position.z + 1, FIRE)

if __name__ == "__main__":
    unittest.main()