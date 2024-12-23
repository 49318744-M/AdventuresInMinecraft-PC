from Builder import Builder
import mcpi.minecraft as minecraft
import mcpi.block as block
import time

class BuildBridge:
    def __init__(self, mc, length, width, height, material, stair_type):
        self.mc = mc
        self.length = length
        self.width = width
        self.height = height
        self.material = material
        self.stair_type = stair_type
        self.name = "BuildBridgeBot"
    
    def build_wall(self, x, y, z, length, height, block_id, direction='x'):
        for i in range(length):
            if direction == 'x':
                self.mc.setBlock(x + i, y, z, block_id)
            else:
                self.mc.setBlock(x, y, z + i, block_id)
        

    def build_feet(self, x, y, z, length, width, block_id):
        start = 3
        y_offset = y - 1  # Start just below the bridge

        for i in range(start, 0, -1):  # Build decreasing rows
            # Front left foot 
            self.build_wall(x, y_offset, z, i, 1, block_id, direction='x')
            # Front right foot 
            self.build_wall(x, y_offset, z + width - 1, i, 1, block_id, direction='x')
            # Back left foot 
            self.build_wall(x + length - i, y_offset, z, i, 1, block_id, direction='x')
            # Back right foot
            self.build_wall(x + length - i, y_offset, z + width - 1, i, 1, block_id, direction='x')

            # Move down one layer
            y_offset -= 1
            time.sleep(0.1) 

    def build_barriers(self, x, y, z, length, width):
        for i in range(length):
            self.mc.setBlock(x + i, y + 1, z, block.FENCE.id)  # Left fence
            self.mc.setBlock(x + i, y + 1, z + width - 1, block.FENCE.id)  # Right fence
            time.sleep(0.1) 

    def build_stairs(self, x, y, z, height, direction, stair_type):
        if direction == 'x':
            for i in range(height):
                self.mc.setBlock(x, y + i, z, block.STAIRS_WOOD.id, 0)  # Stairs going up
                x += 1  # Move one block forward in the stair direction
        else: 
            for i in range(height):
                self.mc.setBlock(x, y + i, z, block.STAIRS_WOOD.id, 1)  # Stairs going down
                x -= 1  # Move one block backward in the stair direction
        time.sleep(0.1)
