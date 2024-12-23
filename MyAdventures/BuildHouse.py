from Builder import Builder
import mcpi.minecraft as minecraft
import mcpi.block as block
import time

class BuildHouse(Builder):
    def __init__(self, mc):
        self.mc = mc
        self.name = "BuildHouseDestroyBot"

    def build_wall(self, x, y, z, length, height, block_id, direction='x'):
        for i in range(length):
            for j in range(height):
                self.mc.setBlock(x + i if direction == 'x' else x,
                                 y + j,
                                 z if direction == 'x' else z + i,
                                 block_id)
                time.sleep(0.05)

    def build_column(self, x, y, z, height, block_id):
        for j in range(height):
            self.mc.setBlock(x, y + j, z, block_id)
            time.sleep(0.05)

    def build_window(self, x, y, z, width, height):
        for i in range(width):
            for j in range(height):
                 self.mc.setBlock(x, y + j, z + i, 102)  # Glass block (id 102)
                 time.sleep(0.05)

    def build_roof(self, x, y, z, width, depth, height, block_id):
        for i in range(height): 
            for j in range(depth):
                # Left slope
                self.mc.setBlock(x + i, y + i, z + j, block_id)
                self.mc.setBlock(x + i - 1, y + i, z + j, block_id)
                time.sleep(0.05)
                # Right slope
                self.mc.setBlock(x + width - i - 1, y + i, z + j, block_id)
                self.mc.setBlock(x + width - i, y + i, z + j, block_id)
                time.sleep(0.05)

        # Add the last line at the top of the roof
        for j in range(depth):
            self.mc.setBlock(x + width // 2, y + height - 1, z + j, block_id)
            time.sleep(0.05)

    def build_filler(self, x, y, z, width, height, block_id):
        for i in range(height):
            for j in range(width - 2 * i):
                self.mc.setBlock(x + i + j, y + i, z, block_id)
                time.sleep(0.05)

    def build_door(self, x, y, z): 
        # Clear space for the door (1x2)
        self.mc.setBlock(x, y - 1, z, 0)  
        self.mc.setBlock(x, y, z, 0)  
        # Place the door
        self.mc.setBlock(x, y - 1, z, 64, 0)  # Door block id
        self.mc.setBlock(x, y, z, 64, 8)  # Door block id
        time.sleep(0.05)

    def add_decorations(self, x, y, z, house_width, house_depth, house_height):
        # Add flower
        flower_height = y + 2
        self.mc.setBlock(x + 3, flower_height, z, 38)  # Flower (id 38)
        self.mc.setBlock(x + 7, flower_height, z, 38)
        time.sleep(0.05)
        
        # Add lanterns
        lantern_height = y + house_height - 1
        self.mc.setBlock(x + 2, lantern_height, z, 50)  # Lantern block id
        self.mc.setBlock(x + 8, lantern_height, z, 50)
        time.sleep(0.05)

        # Window
        self.mc.setBlock(x + 5, y + 7, z, 102)  # Glass block (id 102)
        self.mc.setBlock(x + 5, y + 6, z, 102)
        self.mc.setBlock(x + 4, y + 7, z, 102)
        self.mc.setBlock(x + 4, y + 6, z, 102)
        self.mc.setBlock(x + 6, y + 7, z, 102)
        self.mc.setBlock(x + 6, y + 6, z, 102)
        time.sleep(0.05)

    def build_stairs(self, x, y, z, direction='z'):
        self.mc.setBlock(x, y, z, 53, 2)  # Stairs (id 53)
        time.sleep(0.05)

    def destroy_wall(self, x, y, z, length, height, direction='x'):
        for i in range(length):
            for j in range(height):
                self.mc.setBlock(x + i if direction == 'x' else x,
                                 y + j,
                                 z if direction == 'x' else z + i,
                                 0)  # Set block to air (id 0)
                time.sleep(0.05)

    def destroy_column(self, x, y, z, height):
        for j in range(height):
            self.mc.setBlock(x, y + j, z, 0)  # Set block to air
            time.sleep(0.05)

    def destroy_window(self, x, y, z, width, height):
        for i in range(width):
            for j in range(height):
                 self.mc.setBlock(x, y + j, z + i, 0)  # Set block to air
                 time.sleep(0.05)

    def destroy_roof(self, x, y, z, width, depth, height):
        for i in range(height): 
            for j in range(depth):
                # Left slope
                self.mc.setBlock(x + i, y + i, z + j, 0)  # Remove block
                self.mc.setBlock(x + i - 1, y + i, z + j, 0)
                # Right slope
                self.mc.setBlock(x + width - i - 1, y + i, z + j, 0)
                self.mc.setBlock(x + width - i, y + i, z + j, 0)

        # Remove the last line at the top of the roof
        for j in range(depth):
            self.mc.setBlock(x + width // 2, y + height - 1, z + j, 0)
            time.sleep(0.05)

    def destroy_filler(self, x, y, z, width, height):
        for i in range(height - 1, -1, -1):  
            for j in range(width - 2 * i):
                self.mc.setBlock(x + i + j, y + i, z, 0)
                time.sleep(0.1)


    def destroy_door(self, x, y, z): 
        self.mc.setBlock(x, y - 1, z, 0)  
        self.mc.setBlock(x, y, z, 0)  
        time.sleep(0.05)

    def destroy_decorations(self, x, y, z, house_width, house_depth, house_height):
        # Remove flower
        self.mc.setBlock(x + 3, y + 2, z, 0)  
        self.mc.setBlock(x + 7, y + 2, z, 0)  
        time.sleep(0.05)
        
        # Remove lanterns
        self.mc.setBlock(x + 2, y + house_height - 1, z, 0)
        self.mc.setBlock(x + 8, y + house_height - 1, z, 0)

        # Remove windows
        self.mc.setBlock(x + 5, y + 7, z, 0)
        self.mc.setBlock(x + 5, y + 6, z, 0)
        self.mc.setBlock(x + 4, y + 7, z, 0)
        self.mc.setBlock(x + 4, y + 6, z, 0)
        self.mc.setBlock(x + 6, y + 7, z, 0)
        self.mc.setBlock(x + 6, y + 6, z, 0)
        time.sleep(0.05)

    def destroy_stairs(self, x, y, z):
        self.mc.setBlock(x, y, z, 0)  # Remove stairs
        time.sleep(0.1)
        

