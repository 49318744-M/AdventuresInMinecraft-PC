import time
from mcpi.block import TNT, FIRE
from MinecraftAgent import MinecraftAgent

class TNTBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("TNTBot", mc)

    def perform_task(self, stop_event):
        try:
            pos = self.mc.player.getTilePos()  # Get current position of the player
            self.mc.setBlock(pos.x, pos.y, pos.z, TNT, 1)  # Place TNT
            time.sleep(1) # Wait a second

            # Ignite the TNT by placing fire next to it
            self.mc.setBlock(pos.x, pos.y, pos.z + 1, FIRE)
            self.send_message("Boom!")

            time.sleep(15)  # Wait for the explosion to happen
            if stop_event.is_set():  # Check if the task was interrupted
                self.send_message("TNT task interrupted.")
        except Exception as e:
            print(f"Caught exception: {e}")  # Línea de depuración
            self.send_message(f"Error getting player position: {e}")