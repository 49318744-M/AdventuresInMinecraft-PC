import time
from mcpi.minecraft import Minecraft
from mcpi.block import TNT, FIRE
from MinecraftAgent import MinecraftAgent

class TNTBot(MinecraftAgent):
    def __init__(self):
        super().__init__("TNTBot")

    def perform_task(self):
        """Place TNT and ignite it in the Minecraft world."""
        pos = self.get_position()  # Get the current position of the agent
        self.mc.setBlock(pos.x, pos.y, pos.z, TNT, 1)  # Place TNT
        time.sleep(1)  # Wait a second

        # Ignite the TNT by placing fire next to it
        self.mc.setBlock(pos.x, pos.y, pos.z + 1, FIRE)  # Place fire next to the TNT
        self.send_message("Boom!")

        time.sleep(3)  # Wait for the explosion to happen
        self.send_message("TNT task completed!")
