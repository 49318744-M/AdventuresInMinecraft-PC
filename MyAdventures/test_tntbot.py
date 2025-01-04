import unittest
from unittest.mock import patch, MagicMock
from mcpi.block import TNT, FIRE
from TNTbot import TNTBot
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestTNTBot(unittest.TestCase):

    @patch('mcpi.minecraft.Minecraft.create')
    @patch('mcpi.minecraft.Minecraft.postToChat')
    def setUp(self, mock_post_to_chat, mock_minecraft_create):
        self.mock_mc = MagicMock()
        mock_minecraft_create.return_value = self.mock_mc

        # Instanciar TNTBot con el mock_mc
        self.tnt_bot = TNTBot(self.mock_mc)

        # Asignar el mock a self.tnt_bot.mc
        self.tnt_bot.mc = self.mock_mc
        self.tnt_bot.mc.player.getTilePos.return_value = MagicMock(x=10, y=64, z=10)

        # Mockear el método setBlock
        self.tnt_bot.mc.setBlock = MagicMock()

        # Mockear el método send_message
        self.tnt_bot.send_message = MagicMock()

    def test_place_tnt(self):
        stop_event = MagicMock()
        stop_event.is_set.return_value = False

        self.tnt_bot.perform_task(stop_event)

        self.tnt_bot.mc.setBlock.assert_any_call(10, 64, 10, TNT, 1)
        self.tnt_bot.mc.setBlock.assert_any_call(10, 64, 11, FIRE)

    def test_stop_task_sends_interrupt_message(self):
        stop_event = MagicMock()
        stop_event.is_set.return_value = True

        self.tnt_bot.perform_task(stop_event)

        self.tnt_bot.send_message.assert_any_call("TNT task interrupted.")

    def test_send_message_boom(self):
        stop_event = MagicMock()
        stop_event.is_set.return_value = False

        self.tnt_bot.perform_task(stop_event)

        self.tnt_bot.send_message.assert_any_call("Boom!")

if __name__ == "__main__":
    unittest.main()