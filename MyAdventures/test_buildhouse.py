import unittest
from unittest.mock import patch, MagicMock
from BuildHouse import BuildHouse
import time
import os
import sys

# Añadir el directorio raíz del proyecto al path para que Python pueda encontrar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestBuildHouse(unittest.TestCase):

    @patch('mcpi.minecraft.Minecraft.create')  # Mockear la creación de Minecraft
    @patch('mcpi.minecraft.Minecraft.postToChat')  # Mockear el método postToChat
    def setUp(self, mock_post_to_chat, mock_minecraft_create):
        # Mockear la instancia de Minecraft
        self.mock_mc = MagicMock()
        mock_minecraft_create.return_value = self.mock_mc

        # Instanciar el BuildHouse
        self.build_house_bot = BuildHouse(self.mock_mc)

    def tearDown(self):
        # Clean up objects after each test
        del self.build_house_bot
        del self.mock_mc

    # Test: Build Wall
    def test_build_wall(self):
        self.build_house_bot.build_wall(10, 10, 10, 5, 3, 1, direction='x')
        # Verify that blocks are placed correctly for a 5x3 wall of material 1
        for i in range(5):  # Length
            for j in range(3):  # Height
                self.mock_mc.setBlock.assert_any_call(10 + i, 10 + j, 10, 1)

    # Test: Build Column
    def test_build_column(self):
        self.build_house_bot.build_column(10, 10, 10, 5, 1)
        # Verify that blocks are placed correctly for a column of height 5
        for j in range(5):
            self.mock_mc.setBlock.assert_any_call(10, 10 + j, 10, 1)

    # Test: Build Window
    def test_build_window(self):
        self.build_house_bot.build_window(10, 10, 10, 3, 2)
        # Verify that blocks are placed correctly for a 3x2 glass window (material 102)
        for i in range(3):
            for j in range(2):
                self.mock_mc.setBlock.assert_any_call(10, 10 + j, 10 + i, 102)

    # Test: Build Roof
    def test_build_roof(self):
        self.build_house_bot.build_roof(10, 10, 10, 5, 3, 2, 1)
        # Verify that roof blocks are placed in a pyramid shape
        for i in range(2):  # Roof height
            for j in range(3):  # Depth
                self.mock_mc.setBlock.assert_any_call(10 + i, 10 + i, 10 + j, 1)
                self.mock_mc.setBlock.assert_any_call(10 + 5 - i - 1, 10 + i, 10 + j, 1)

    # Test: Build Door
    def test_build_door(self):
        self.build_house_bot.build_door(10, 10, 10)
        # Verify that a door (material 64) is placed correctly
        self.mock_mc.setBlock.assert_any_call(10, 10 - 1, 10, 0)  # Clear the lower block
        self.mock_mc.setBlock.assert_any_call(10, 10, 10, 64, 8)  # Place upper part of the door

    # Test: Add Decorations
    def test_add_decorations(self):
        self.build_house_bot.add_decorations(10, 10, 10, 10, 10, 10)
        # Verify decorations are added (flowers, lanterns, etc.)
        self.mock_mc.setBlock.assert_any_call(10 + 3, 12, 10, 38)  # Flower
        self.mock_mc.setBlock.assert_any_call(10 + 7, 12, 10, 38)
        self.mock_mc.setBlock.assert_any_call(10 + 2, 19, 10, 50)  # Lantern
        self.mock_mc.setBlock.assert_any_call(10 + 8, 19, 10, 50)

    # Test: Build Stairs
    def test_build_stairs(self):
        self.build_house_bot.build_stairs(10, 10, 10)
        # Verify stairs are placed correctly
        self.mock_mc.setBlock.assert_any_call(10, 10, 10, 53 , 2)

    # Test: Perform Task
    def test_perform_task(self):
        # Simulate the player's position
        self.mock_mc.player.getTilePos.return_value = MagicMock(x=0, y=10, z=0)
        stop_event = MagicMock()
        stop_event.is_set.return_value = False

        # Run the task
        self.build_house_bot.perform_task(stop_event)
        # Ensure house-building methods were executed
        self.assertTrue(self.mock_mc.setBlock.called)


if __name__ == "__main__":
    unittest.main()