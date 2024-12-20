import time
import mcpi.minecraft as minecraft
import mcpi.block as block

class BuildDestroy:
    def __init__(self, mc):
        self.mc = mc
        self.name = "BuildDestroyBot"

    def move_to(self, x, y, z):
        self.mc.player.setTilePos(x, y, z)

    def build_wall(self, x, y, z, length, height, block_id, direction='x'):
        if direction == 'x':  # Build in direction X
            for i in range(length):
                for j in range(height):
                    self.mc.setBlock(x + i, y + j, z, block_id)  # Direction X
                    time.sleep(0.1)
                    
        elif direction == 'z':  # Build in direction Z
            for i in range(length):
                for j in range(height):
                    self.mc.setBlock(x, y + j, z + i, block_id)  # Direction Z
                    time.sleep(0.1)

    def run(self):
        time.sleep(2)
        self.mc.postToChat(f"{self.name} starting!")
        pos = self.mc.player.getTilePos()

        # Position to start building the square
        offset_x = pos.x + 5
        offset_z = pos.z

        # Build the 4 walls of the square
        # Wall 1: In direction X (h)
        self.build_wall(offset_x, pos.y, offset_z, 5, 3, block.STONE.id, direction='x')
        # Wall 2: In direction Z (v)
        self.build_wall(offset_x, pos.y, offset_z, 5, 3, block.STONE.id, direction='z')
        # Wall 3: In direction X (h) 
        self.build_wall(offset_x, pos.y, offset_z + 4, 5, 3, block.STONE.id, direction='x')
        # Wall 4: In direction Z (v)
        self.build_wall(offset_x + 4, pos.y, offset_z, 5, 3, block.STONE.id, direction='z')

        self.mc.postToChat(f"{self.name} has finished building the 4 walls of the house.")

# Code to test the bot
if __name__ == "__main__":
    # Connect to the Minecraft server
    mc = minecraft.Minecraft.create()

    # Create an instance of the bot
    bot = BuildDestroy(mc)

    # Run the bots
    bot.run()
    time.sleep(10)  # Pause for 10 seconds before ending the program
