import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BotManager import BotManager

class TestBotManager(unittest.IsolatedAsyncioTestCase):
    def test_add_agent(self):
        self.mock_mc = MagicMock()
        self.bot_manager = BotManager(self.mock_mc)

        self.mock_bot1 = AsyncMock()
        self.mock_bot2 = AsyncMock()
        self.mock_bot1.name = "bot1"
        self.mock_bot2.name = "bot2"

        self.bot_manager.add_agent("bot1", self.mock_bot1)
        self.bot_manager.add_agent("bot2", self.mock_bot2)

        self.assertIn("bot1", self.bot_manager.agents)
        self.assertIn("bot2", self.bot_manager.agents)
        self.assertEqual(self.bot_manager.agents["bot1"], self.mock_bot1)
        self.assertEqual(self.bot_manager.agents["bot2"], self.mock_bot2)

    async def test_list_agents(self):
        self.mock_mc = MagicMock()
        self.bot_manager = BotManager(self.mock_mc)

        self.mock_bot1 = AsyncMock()
        self.mock_bot2 = AsyncMock()
        self.mock_bot1.name = "bot1"
        self.mock_bot2.name = "bot2"

        self.bot_manager.add_agent("bot1", self.mock_bot1)
        self.bot_manager.add_agent("bot2", self.mock_bot2)

        agents = await self.bot_manager.list_agents()
        self.assertEqual(agents, ["bot1", "bot2"])

    @patch("asyncio.create_task")
    async def test_handle_command_start_bot(self, mock_create_task):
        self.mock_mc = MagicMock()
        self.bot_manager = BotManager(self.mock_mc)

        self.mock_bot1 = AsyncMock()
        self.mock_bot2 = AsyncMock()
        self.mock_bot1.name = "bot1"
        self.mock_bot2.name = "bot2"

        self.bot_manager.add_agent("bot1", self.mock_bot1)
        self.bot_manager.add_agent("bot2", self.mock_bot2)

        message = "bot1"
        await self.bot_manager.handle_command(message)

        mock_create_task.assert_called_once()
        self.mock_bot1.perform_task.assert_called_once()

    @patch("asyncio.create_task")
    async def test_handle_command_switch_bot(self, mock_create_task):
        self.mock_mc = MagicMock()
        self.bot_manager = BotManager(self.mock_mc)

        self.mock_bot1 = AsyncMock()
        self.mock_bot2 = AsyncMock()
        self.mock_bot1.name = "bot1"
        self.mock_bot2.name = "bot2"

        self.bot_manager.add_agent("bot1", self.mock_bot1)
        self.bot_manager.add_agent("bot2", self.mock_bot2)

        task_mock = MagicMock()
        task_mock.cancel = MagicMock()
        self.mock_bot1.perform_task.return_value = task_mock

        message_start_bot1 = "bot1"
        await self.bot_manager.handle_command(message_start_bot1)

        message_switch_bot = "bot2"
        await self.bot_manager.handle_command(message_switch_bot)

        task_mock.cancel.assert_called_once()
        mock_create_task.assert_called_with(self.mock_bot2.perform_task(AsyncMock()))

    async def test_handle_command_invalid_command(self):
        self.mock_mc = MagicMock()
        self.bot_manager = BotManager(self.mock_mc)

        message = "unknown_command"
        await self.bot_manager.handle_command(message)

        self.mock_mc.postToChat.assert_called_once_with("Unknown command: unknown_command")

    @patch("asyncio.create_task")
    async def test_handle_command_list(self, _):
        self.mock_mc = MagicMock()
        self.bot_manager = BotManager(self.mock_mc)

        self.mock_bot1 = AsyncMock()
        self.mock_bot2 = AsyncMock()
        self.mock_bot1.name = "bot1"
        self.mock_bot2.name = "bot2"

        self.bot_manager.add_agent("bot1", self.mock_bot1)
        self.bot_manager.add_agent("bot2", self.mock_bot2)

        message = "list"
        await self.bot_manager.handle_command(message)

        self.mock_mc.postToChat.assert_called_once_with("Available agents: bot1, bot2")

    async def test_listen_for_commands(self):
        self.mock_mc = MagicMock()
        self.bot_manager = BotManager(self.mock_mc)

        def poll_chat_events():
            yield [MagicMock(message="bot1")]
            yield []

        self.mock_mc.events.pollChatPosts.side_effect = poll_chat_events()

        with patch("asyncio.sleep", return_value=None):
            try:
                await asyncio.wait_for(self.bot_manager.listen_for_commands(), timeout=0.1)
            except StopIteration:
                pass

        self.mock_bot1 = self.bot_manager.agents["bot1"]
        self.mock_bot1.perform_task.assert_called_once()


if __name__ == "__main__":
    unittest.main()