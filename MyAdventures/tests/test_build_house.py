import unittest
from unittest.mock import MagicMock, call
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BuildHouse import BuildHouse

class TestBuildHouse(unittest.TestCase):
    def setUp(self):
        self.mc_mock = MagicMock()
        self.builder = BuildHouse(self.mc_mock)
        self.builder.send_message = MagicMock()

    # Test 1: Verify wall building 
    def test_build_wall(self):
        x, y, z = 0, 0, 0
        length, height = 5, 3
        block_id = 1  # Example 

        self.builder.build_wall(x, y, z, length, height, block_id)

        expected_calls = [
            call.setBlock(x + i, y + j, z, block_id)
            for i in range(length)
            for j in range(height)
        ]
        self.assertEqual(self.mc_mock.setBlock.call_args_list, expected_calls)

    # Test 2: Verify column building 
    def test_build_column(self):
        x, y, z = 0, 0, 0
        height = 3
        block_id = 1

        self.builder.build_column(x, y, z, height, block_id)

        expected_calls = [
            call.setBlock(x, y + j, z, block_id)
            for j in range(height)
        ]
        self.assertEqual(self.mc_mock.setBlock.call_args_list, expected_calls)

    # Test 3: Verify window building 
    def test_build_window(self):
        x, y, z = 0, 0, 0
        width, height = 2, 2

        self.builder.build_window(x, y, z, width, height)

        expected_calls = [
            call.setBlock(x, y + j, z + i, 102)  # Glass block ID
            for i in range(width)
            for j in range(height)
        ]
        self.assertEqual(self.mc_mock.setBlock.call_args_list, expected_calls)

    # Test 4: Verify roof building 
    def test_build_roof(self):
        x, y, z = 0, 0, 0
        width, depth, height = 5, 5, 3
        block_id = 17  # Example 

        self.builder.build_roof(x, y, z, width, depth, height, block_id)

        expected_calls = []
        for i in range(height):
            for j in range(depth):
                expected_calls.append(call.setBlock(x + i, y + i, z + j, block_id))
                expected_calls.append(call.setBlock(x + i - 1, y + i, z + j, block_id))
                expected_calls.append(call.setBlock(x + width - i - 1, y + i, z + j, block_id))
                expected_calls.append(call.setBlock(x + width - i, y + i, z + j, block_id))
        for j in range(depth):
            expected_calls.append(call.setBlock(x + width // 2, y + height - 1, z + j, block_id))

        self.assertEqual(self.mc_mock.setBlock.call_args_list, expected_calls)

    # Test 5: Verify door building
    def test_build_door(self):
        x, y, z = 0, 0, 0

        self.builder.build_door(x, y, z)

        expected_calls = [
            call.setBlock(x, y - 1, z, 0),
            call.setBlock(x, y, z, 0),
            call.setBlock(x, y - 1, z, 64, 0),
            call.setBlock(x, y, z, 64, 8)
        ]
        self.assertEqual(self.mc_mock.setBlock.call_args_list, expected_calls)

    # Test 6: Verify decoration 
    def test_add_decorations(self):
        x, y, z = 0, 0, 0
        house_width, house_depth, house_height = 5, 5, 5

        self.builder.add_decorations(x, y, z, house_width, house_depth, house_height)

        expected_calls = [
            call.setBlock(x + 3, y + 2, z, 38),
            call.setBlock(x + 7, y + 2, z, 38),
            call.setBlock(x + 2, y + house_height - 1, z, 50),
            call.setBlock(x + 8, y + house_height - 1, z, 50),
            call.setBlock(x + 5, y + 7, z, 102),
            call.setBlock(x + 5, y + 6, z, 102),
            call.setBlock(x + 4, y + 7, z, 102),
            call.setBlock(x + 4, y + 6, z, 102),
            call.setBlock(x + 6, y + 7, z, 102),
            call.setBlock(x + 6, y + 6, z, 102)
        ]
        self.assertEqual(self.mc_mock.setBlock.call_args_list, expected_calls)

    # Test 7: Verify stairs building 
    def test_build_stairs(self):
        x, y, z = 0, 0, 0
        direction = 'z'

        self.builder.build_stairs(x, y, z, direction)

        expected_calls = [
            call.setBlock(x, y, z, 53, 2)  
        ]
        self.assertEqual(self.mc_mock.setBlock.call_args_list, expected_calls)

if __name__ == '__main__':
    unittest.main()