import asyncio
from MinecraftAgent import MinecraftAgent
from mcpi import block

class ReflectiveBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("ReflectiveBot", mc)

    def greet(self):
        self.send_message("Hello, I'm your reflective bot")

    def bye(self):
        self.send_message("Bye, see you next time!")

    def help(self):
        self.send_message("Available commands: greet, help, joke, bye, place_block")

    def joke(self):
        self.send_message("joke joke joke.")

    def place_block(self):
        pos = self.mc.player.getTilePos()
        self.mc.setBlock(pos.x, pos.y - 1, pos.z, block.DIAMOND_BLOCK.id)
        self.send_message("Placed a diamond block under your feet!")

    def __getattr__(self, attr):
        return lambda *args, **kwargs: self.send_message(f"Unknown method or command '{attr}'")

    async def perform_task(self, stop_event):
        self.send_message("ReflectiveBot is active. Type 'reflective <command>' to interact.")
        self.help()

        while not stop_event.is_set():
            await asyncio.sleep(1)

        self.send_message("ReflectiveBot has been interrupted.")

    def respond(self, command):
        
        if hasattr(self, command):
            getattr(self, command)()  # Llama a greet, joke, etc.
        else:
            self.mc.postToChat(f"Unknown command: {command}")