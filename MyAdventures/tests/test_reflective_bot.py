import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ReflectiveBot import ReflectiveBot

class TestReflectiveBot(unittest.IsolatedAsyncioTestCase):
    # Test 1: Greet
    async def test_greet(self):
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)
        with patch.object(bot, 'send_message_async', new=AsyncMock()) as mock_send:
            await bot.greet()
            mock_send.assert_awaited_once_with("Hello, I'm your reflective bot")

    # Test 2: Bye
    async def test_bye(self):
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)
        with patch.object(bot, 'send_message_async', new=AsyncMock()) as mock_send:
            await bot.bye()
            mock_send.assert_awaited_once_with("Bye, see you next time!")

    # Test 3: Help
    async def test_help(self):
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)
        with patch.object(bot, 'send_message_async', new=AsyncMock()) as mock_send:
            await bot.help()
            mock_send.assert_awaited_once_with(
                "Available commands: greet, help, joke, bye, place_block"
            )

    # Test 4: Joke
    async def test_joke(self):
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)
        with patch.object(bot, 'send_message_async', new=AsyncMock()) as mock_send:
            await bot.joke()
            mock_send.assert_awaited_once_with("joke joke joke.")

    # Test 5: Place_block
    async def test_place_block(self):
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)
        with patch.object(bot, 'send_message_async', new=AsyncMock()) as mock_send:
        
            pos_mock = MagicMock()
            pos_mock.x = 10
            pos_mock.y = 64
            pos_mock.z = 10
            mc_mock.player.getTilePos.return_value = pos_mock

            with patch('mcpi.block.DIAMOND_BLOCK.id', new=57):
                await bot.place_block()
                mc_mock.setBlock.assert_called_with(10, 63, 10, 57)
                mock_send.assert_awaited_once_with("Placed a diamond block under your feet!")


    # Test 6: Interrupt functionality
    async def test_interrupt_functionality(self):
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)
        stop_event = asyncio.Event()
        with patch.object(bot, 'send_message_async', new=AsyncMock()) as mock_send:
            task = asyncio.create_task(bot.perform_task(stop_event))
            await asyncio.sleep(0.1)  
            stop_event.set()  
