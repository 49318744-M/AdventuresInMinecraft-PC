import asyncio
from MinecraftAgent import MinecraftAgent

class TNTBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("TNTBot", mc)

    async def perform_task(self, stop_event):
        try:
            while not stop_event.is_set():
                pos = self.mc.player.getTilePos()
                self.mc.setBlock(pos.x, pos.y, pos.z, 46)  # TNT block
                await self.send_message("Boom!")
                await asyncio.sleep(5)
        except Exception as e:
            await self.send_message(f"Error getting player position: {e}")
        finally:
            await self.send_message("TNT task interrupted.")