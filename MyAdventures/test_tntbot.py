import unittest
from unittest.mock import MagicMock
from mcpi.block import TNT, FIRE
from TNTbot import TNTBot  # Assuming the TNTBot class is in TNTBot.py
import time

class TestTNTBot(unittest.TestCase):

    def setUp(self):
        #Mock to avoid interacting with real Minecraft
        self.mock_mc = MagicMock()

        # Instantiate the TNTBot
        self.tnt_bot = TNTBot()

        # Mock mc.player.getTilePos to return a fixed position
        self.tnt_bot.mc = self.mock_mc
        self.tnt_bot.mc.player.getTilePos.return_value = MagicMock(x=10, y=64, z=10)

        # Mock the setBlock method to avoid actual block placement
        self.tnt_bot.mc.setBlock = MagicMock()

        # Mock the send_message method
        self.tnt_bot.send_message = MagicMock()

    def test_place_tnt(self): #simulate the placement of TNT and fire
        # Ensure that doesnt stop
        stop_event = MagicMock()
        stop_event.is_set.return_value = False

        # Execute the perform_task method
        self.tnt_bot.perform_task(stop_event)

        # Verify that TNT was placed at the correct position (10, 64, 10)
        self.tnt_bot.mc.setBlock.assert_any_call(10, 64, 10, TNT, 1)

        # Verify that fire was placed at (10, 64, 11) using the correct FIRE block object
        self.tnt_bot.mc.setBlock.assert_any_call(10, 64, 11, FIRE)

    def test_stop_task_sends_interrupt_message(self): #simulate the interruption of the bot
        # Now we simulate the interruption
        stop_event = MagicMock()
        stop_event.is_set.return_value = True

        # Execute the perform_task method
        self.tnt_bot.perform_task(stop_event)

        # Verify that the user interrupted the bot
        self.tnt_bot.send_message.assert_any_call("TNT task interrupted.")

    def test_send_message_boom(self): #simulate the Boom message
        stop_event = MagicMock()
        stop_event.is_set.return_value = False

        # Execute the perform_task method
        self.tnt_bot.perform_task(stop_event)

        # Verify that "Boom!" message was sent
        self.tnt_bot.send_message.assert_any_call("Boom!")


if __name__ == "__main__":
    unittest.main()
