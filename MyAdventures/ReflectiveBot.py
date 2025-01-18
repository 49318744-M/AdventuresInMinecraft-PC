import time
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
        self.send_message(
            "Available commands: greet, help, joke, bye, place_block"
        )

    def joke(self):
        self.send_message("joke joke joke.")

    def place_block(self):
        pos = self.mc.player.getTilePos()
        self.mc.setBlock(pos.x, pos.y - 1, pos.z, block.DIAMOND_BLOCK.id)
        self.send_message("Placed a diamond block under your feet!")

    def __getattr__(self, attr):
        # Fallback para comandos desconocidos
        return lambda *args, **kwargs: self.send_message(
            f"Unknown method or command '{attr}'"
        )

    async def perform_task(self, stop_event):
        self.send_message("ReflectiveBot is active. Use 'reflective <command>' to interact.")
        self.help()  # Send instructions on how to use the bot
        while not stop_event.is_set():
            chat_events = self.mc.events.pollChatPosts()
            for event in chat_events:
                if stop_event.is_set():
                    return
                message = event.message.strip().lower()
                if message.startswith("reflective "):
                    command = message.split("reflective ")[1]
                    self.respond(command)
                elif message in self.agents:  # Verificar si el mensaje es el nombre de otro bot
                    stop_event.set()  # Detener el ReflectiveBot
                    self.send_message(f"Stopping ReflectiveBot and switching to {message}.")
                    return
            await asyncio.sleep(0.1)
        self.send_message("ReflectiveBot has been interrupted.")

    def respond(self, command):
        if hasattr(self, command):
            getattr(self, command)()
        else:
            self.mc.postToChat(f"Unknown command: {command}")