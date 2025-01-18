import asyncio
from mcpi.block import TNT, FIRE
from MinecraftAgent import MinecraftAgent

class TNTBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("TNTBot", mc)

    async def perform_task(self, stop_event):
        try:
            pos = self.mc.player.getTilePos()  # Player position
            self.mc.setBlock(pos.x, pos.y, pos.z, TNT, 1)  # Place tnt
            await asyncio.sleep(1)  # wait

            # Fire the tnt
            self.mc.setBlock(pos.x, pos.y, pos.z + 1, FIRE)
            self.send_message("Boom!")

            await asyncio.sleep(15)  
            if stop_event.is_set():  # if interrupted
                self.send_message("TNT task interrupted.")
        except Exception as e:
            print(f"Caught exception: {e}")  
            self.send_message(f"Error getting player position: {e}")