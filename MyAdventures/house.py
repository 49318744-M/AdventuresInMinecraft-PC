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

    def build_column(self, x, y, z, height, block_id):
        for j in range(height):
            self.mc.setBlock(x, y + j, z, block_id)

    def build_window(self, x, y, z, width, height):
        for i in range(width):
            for j in range(height):
                 self.mc.setBlock(x, y + j, z + i, 102)   # id for Glass block


    def build_roof(self, x, y, z, width, depth, height, block_id):
        for i in range(height): 
            for j in range(depth):
                # Left slope
                self.mc.setBlock(x + i, y + i, z + j, block_id)
                self.mc.setBlock(x + i - 1, y + i, z + j, block_id)
                # Right slope
                self.mc.setBlock(x + width - i - 1, y + i, z + j, block_id)
                self.mc.setBlock(x + width - i, y + i, z + j, block_id)

        # Add the last line at the top of the roof
        for j in range(depth):
            self.mc.setBlock(x + width // 2, y + height - 1, z + j, block_id)

    def build_filler(self, x, y, z, width, height, block_id):
        for i in range(height):
            for j in range(width - 2 * i):
                self.mc.setBlock(x + i + j, y + i, z, block_id)
                time.sleep(0.1)
            

    def build_door(self, x, y, z): 
        # Clear space for the door (1x2)
        self.mc.setBlock(x, y - 1, z, 0)  
        self.mc.setBlock(x, y, z, 0)  
        # Place the door
        self.mc.setBlock(x, y - 1, z, 64, 0)
        self.mc.setBlock(x, y, z, 64, 8)  



    def add_decorations(self, x, y, z, house_width, house_depth, house_height):
        # Add flower
        flower_height = y + 2
        self.mc.setBlock(x + 3, flower_height, z, 38)  # Flower (id 38)
        self.mc.setBlock(x + 7, flower_height, z, 38)  

        # Add lanterns
        lantern_height = y + house_height - 1
        self.mc.setBlock(x + 2, lantern_height, z, 50)
        self.mc.setBlock(x + 8, lantern_height, z, 50)

        #Window
        self.mc.setBlock(x + 5, y + 7, z, 102)
        self.mc.setBlock(x + 5, y + 6, z, 102)
        self.mc.setBlock(x + 4, y + 7, z, 102)
        self.mc.setBlock(x + 4, y + 6, z, 102)
        self.mc.setBlock(x + 6, y + 7, z, 102)
        self.mc.setBlock(x + 6, y + 6, z, 102)

    def build_stairs(self, x, y, z, direction='z'):
        self.mc.setBlock(x, y, z, 53, 2)

    def run(self):
        time.sleep(2)
        self.mc.postToChat(f"{self.name} starting!")
        pos = self.mc.player.getTilePos()

        # New position to start building the house
        offset_x = pos.x + 5
        offset_z = pos.z

        # Dimensions of the house
        house_width = 11
        house_depth = 10
        house_height = 7
        roof_height = 5

        # Build the 4 walls of stone (id: 98)
        self.build_wall(offset_x, pos.y, offset_z, house_width, house_height, 98, direction='x')
        self.build_wall(offset_x, pos.y, offset_z, house_depth, house_height, 98, direction='z')
        self.build_wall(offset_x, pos.y, offset_z + house_depth, house_width, house_height, 98, direction='x')
        self.build_wall(offset_x + house_width - 1, pos.y, offset_z, house_depth, house_height, 98, direction='z')

        # Build columns at the 4 corners in pink (id: 201)
        self.build_column(offset_x, pos.y, offset_z, house_height, 201)
        self.build_column(offset_x + house_width - 1, pos.y, offset_z, house_height, 201)
        self.build_column(offset_x, pos.y, offset_z + house_depth, house_height, 201)
        self.build_column(offset_x + house_width - 1, pos.y, offset_z + house_depth, house_height, 201)

        # Add windows
        self.build_window(offset_x, pos.y + 2, offset_z + 2, 3, 3)  # Left wall window 1
        self.build_window(offset_x, pos.y + 2, offset_z + house_depth - 4, 3, 3)  # Left wall window 2
        self.build_window(offset_x + 4 + house_width - 5, pos.y + 2, offset_z + 2, 3, 3)  # Right wall window 1
        self.build_window(offset_x + 4 + house_width - 5, pos.y + 2, offset_z + house_depth - 4, 3, 3)  # Right wall window 2


        # Build a filler between the wall and the roof
        self.build_filler(offset_x, pos.y + house_height, offset_z, house_width, roof_height - 1, 98)
        self.build_filler(offset_x, pos.y + house_height, offset_z + house_depth, house_width, roof_height - 1, 98)

        # Build the roof 
        self.build_roof(offset_x, pos.y + house_height, offset_z - 1, house_width, house_depth + 3, roof_height, 17)


        # Build a door
        self.build_door(offset_x + 5, pos.y + 2, offset_z)

        # Add decorations
        self.add_decorations(offset_x, pos.y, offset_z, house_width, house_depth, house_height)

        #Stairs
        self.build_stairs(offset_x + 5, pos.y, offset_z - 1, direction='z')  
        self.build_stairs(offset_x + 4, pos.y, offset_z - 1, direction='z')  
        self.build_stairs(offset_x + 6, pos.y, offset_z - 1, direction='z') 


        

# Code to execute the bot
if __name__ == "__main__":
    # Connect to the Minecraft server
    mc = minecraft.Minecraft.create()

    # Create an instance of the bot
    bot = BuildDestroy(mc)

    # Run the bot's actions
    bot.run()
    time.sleep(10)  # Pause for 10 seconds before ending the program
