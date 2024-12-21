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
                self.mc.setBlock(x + i, y + j, z, 102)  # id for Glass block

    def run(self):
        time.sleep(2)
        self.mc.postToChat(f"{self.name} starting!")
        pos = self.mc.player.getTilePos()

        # New position to start building the house
        offset_x = pos.x + 5
        offset_z = pos.z

        # Build the 4 walls of stone (id: 98)
        self.build_wall(offset_x, pos.y, offset_z, 11, 7, 98, direction='x')
        self.build_wall(offset_x, pos.y, offset_z, 10, 7, 98, direction='z') 
        self.build_wall(offset_x, pos.y, offset_z + 10, 11, 7, 98, direction='x')  
        self.build_wall(offset_x + 11, pos.y, offset_z, 10, 7, 98, direction='z')  

        # Build columns at the 4 corners in pink (id: 201)
        self.build_column(offset_x, pos.y, offset_z, 7, 201)
        self.build_column(offset_x + 11, pos.y, offset_z, 7, 201)
        self.build_column(offset_x, pos.y, offset_z + 10, 7, 201)
        self.build_column(offset_x + 11, pos.y, offset_z + 10, 7, 201)

        # Add windows
        self.build_window(offset_x + 2, pos.y + 2, offset_z, 3, 3)
        self.build_window(offset_x + 7, pos.y + 2, offset_z, 3, 3)
        self.build_window(offset_x + 2, pos.y + 2, offset_z + 10, 3, 3)
        self.build_window(offset_x + 7, pos.y + 2, offset_z + 10, 3, 3)

        self.mc.postToChat(f"{self.name} has finished building the house")

# Code to execute the bot
if __name__ == "__main__":
    # Connect to the Minecraft server
    mc = minecraft.Minecraft.create()

    # Create an instance of the bot
    bot = BuildDestroy(mc)

    # Run the bot's actions
    bot.run()
    time.sleep(10)  # Pause for 10 seconds before ending the program

