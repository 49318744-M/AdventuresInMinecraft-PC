import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BotManager import BotManager

class TestBotManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_mc = MagicMock()
        self.bot_manager = BotManager(self.mock_mc)

    # Test 1: adding agents
    def test_add_agent(self):
        mock_bot1 = AsyncMock()
        mock_bot2 = AsyncMock()
        mock_bot1.name = "bot1"
        mock_bot2.name = "bot2"

        self.bot_manager.add_agent("bot1", mock_bot1)
        self.bot_manager.add_agent("bot2", mock_bot2)

        self.assertIn("bot1", self.bot_manager.agents)
        self.assertIn("bot2", self.bot_manager.agents)
        self.assertEqual(self.bot_manager.agents["bot1"], mock_bot1)
        self.assertEqual(self.bot_manager.agents["bot2"], mock_bot2)

    # Test 2: list of added agents
    async def test_list_agents(self):
        mock_bot1 = AsyncMock()
        mock_bot2 = AsyncMock()
        mock_bot1.name = "bot1"
        mock_bot2.name = "bot2"

        self.bot_manager.add_agent("bot1", mock_bot1)
        self.bot_manager.add_agent("bot2", mock_bot2)

        agents = await self.bot_manager.list_agents()
        self.assertEqual(agents, ["bot1", "bot2"])

    # Test 3: handle command to start a bot
    @patch("asyncio.create_task")
    async def test_handle_command_start_bot(self, mock_create_task):
        mock_bot1 = AsyncMock()
        mock_bot2 = AsyncMock()
        mock_bot1.name = "bot1"
        mock_bot2.name = "bot2"

        mock_bot1.perform_task = MagicMock()
        mock_bot2.perform_task = MagicMock()

        self.bot_manager.add_agent("bot1", mock_bot1)
        self.bot_manager.add_agent("bot2", mock_bot2)

        message = "bot1"
        await self.bot_manager.handle_command(message)

        mock_create_task.assert_called_once()
        mock_bot1.perform_task.assert_called_once()

    # Test 4: switching bots
    @patch("asyncio.create_task")
    async def test_handle_command_switch_bot(self, mock_create_task):
        mock_bot1 = AsyncMock()
        mock_bot2 = AsyncMock()
        mock_bot1.name = "bot1"
        mock_bot2.name = "bot2"

        mock_bot1.perform_task = MagicMock()
        mock_bot2.perform_task = MagicMock()

        self.bot_manager.add_agent("bot1", mock_bot1)
        self.bot_manager.add_agent("bot2", mock_bot2)

        await self.bot_manager.handle_command("bot1")
        await self.bot_manager.handle_command("bot2")

        self.assertTrue(mock_bot1.perform_task.called)
        self.assertTrue(mock_bot2.perform_task.called)
        self.assertEqual(mock_create_task.call_count, 2)

    # Test 5: handle unknown commands
    async def test_handle_command_invalid_command(self):
        message = "unknown_command"
        await self.bot_manager.handle_command(message)
        self.mock_mc.postToChat.assert_called_once_with("Unknown command: unknown_command")

    # Test 6: post list of available agents
    @patch("asyncio.create_task")
    async def test_handle_command_list(self, mock_create_task):
        mock_bot1 = AsyncMock()
        mock_bot2 = AsyncMock()
        mock_bot1.name = "bot1"
        mock_bot2.name = "bot2"

        self.bot_manager.add_agent("bot1", mock_bot1)
        self.bot_manager.add_agent("bot2", mock_bot2)

        message = "list"
        await self.bot_manager.handle_command(message)

        self.mock_mc.postToChat.assert_called_once_with("Available agents: bot1, bot2")

    # Test 7: Reflective commands
    @patch("asyncio.create_task")
    async def test_handle_command_reflective_command(self, mock_create_task):
        reflect_bot_mock = AsyncMock()
        reflect_bot_mock.name = "reflective"

        reflect_bot_mock.perform_task = MagicMock()
        
        reflect_bot_mock.respond = MagicMock()

        self.bot_manager.add_agent("reflective", reflect_bot_mock)

        await self.bot_manager.handle_command("reflective")
        self.assertEqual(self.bot_manager.current_agent_name, "reflective")
        self.mock_mc.postToChat.reset_mock()
        message = "reflective greet"
        await self.bot_manager.handle_command(message)

        reflect_bot_mock.respond.assert_called_once_with("greet")

        calls = [call[0][0] for call in self.mock_mc.postToChat.call_args_list]
        self.assertNotIn("Unknown command: reflective greet", calls)


if __name__ == "__main__":
    unittest.main()