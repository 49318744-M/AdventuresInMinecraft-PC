import time
import mcpi.minecraft as minecraft
import mcpi.block as block

class BuildDestroy:
    def __init__(self, mc):
        self.mc = mc
        self.name = "BuildDestroyBot"

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

    def build_house(self, x, y, z, house_width, house_depth, house_height, roof_height):
        # Build walls
        self.build_wall(x, y, z, house_width, house_height, 98, direction='x')
        self.build_wall(x, y, z, house_depth, house_height, 98, direction='z')
        self.build_wall(x, y, z + house_depth, house_width, house_height, 98, direction='x')
        self.build_wall(x + house_width - 1, y, z, house_depth, house_height, 98, direction='z')

        # Build columns at the 4 corners in pink (id: 201)
        self.build_column(x, y, z, house_height, 201)
        self.build_column(x + house_width - 1, y, z, house_height, 201)
        self.build_column(x, y, z + house_depth, house_height, 201)
        self.build_column(x + house_width - 1, y, z + house_depth, house_height, 201)

        # Add windows
        self.build_window(x, y + 2, z + 2, 3, 3)
        self.build_window(x, y + 2, z + house_depth - 4, 3, 3)
        self.build_window(x + 4 + house_width - 5, y + 2, z + 2, 3, 3)
        self.build_window(x + 4 + house_width - 5, y + 2, z + house_depth - 4, 3, 3)

        # Build filler between the wall and the roof
        self.build_filler(x, y + house_height, z, house_width, roof_height - 1, 98)
        self.build_filler(x, y + house_height, z + house_depth, house_width, roof_height - 1, 98)

        # Build the roof
        self.build_roof(x, y + house_height, z - 1, house_width, house_depth + 3, roof_height, 17)

        # Build door
        self.build_door(x + 5, y + 2, z)

        # Add decorations
        self.add_decorations(x, y, z, house_width, house_depth, house_height)

        # Build stairs
        self.build_stairs(x + 5, y, z - 1, direction='z')  
        self.build_stairs(x + 4, y, z - 1, direction='z')  
        self.build_stairs(x + 6, y, z - 1, direction='z')  

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
        for i in range(height - 1, -1, -1):  # Comienza desde la parte superior (height-1) y recorre hacia abajo
            for j in range(width - 2 * i):
                self.mc.setBlock(x + i + j, y + i, z, 0)  # Remueve el bloque
                time.sleep(0.1)


    def destroy_door(self, x, y, z): 
        # Remove door blocks
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

    def destroy_house(self, x, y, z, house_width, house_depth, house_height, roof_height):
        # Destroy stairs
        self.destroy_stairs(x + 5, y, z - 1)
        self.destroy_stairs(x + 4, y, z - 1)
        self.destroy_stairs(x + 6, y, z - 1)

        # Destroy decorations
        self.destroy_decorations(x, y, z, house_width, house_depth, house_height)

        # Destroy door
        self.destroy_door(x + 5, y + 2, z)

        # Destroy roof
        self.destroy_roof(x, y + house_height, z - 1, house_width, house_depth + 3, roof_height)

        # Destroy filler between the wall and the roof
        self.destroy_filler(x, y + house_height, z, house_width, roof_height - 1)
        self.destroy_filler(x, y + house_height, z + house_depth, house_width, roof_height - 1)

        # Destroy windows
        self.destroy_window(x, y + 2, z + 2, 3, 3)
        self.destroy_window(x, y + 2, z + house_depth - 4, 3, 3)
        self.destroy_window(x + 4 + house_width - 5, y + 2, z + 2, 3, 3)
        self.destroy_window(x + 4 + house_width - 5, y + 2, z + house_depth - 4, 3, 3)

        # Destroy columns at the 4 corners
        self.destroy_column(x, y, z, house_height)
        self.destroy_column(x + house_width - 1, y, z, house_height)
        self.destroy_column(x, y, z + house_depth, house_height)
        self.destroy_column(x + house_width - 1, y, z + house_depth, house_height)

        # Destroy walls
        self.destroy_wall(x, y, z, house_width, house_height, direction='x')
        self.destroy_wall(x, y, z, house_depth, house_height, direction='z')
        self.destroy_wall(x, y, z + house_depth, house_width, house_height, direction='x')
        self.destroy_wall(x + house_width - 1, y, z, house_depth, house_height, direction='z')

