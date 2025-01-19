import asyncio
from MinecraftAgent import MinecraftAgent
from mcpi import block

class ReflectiveBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("ReflectiveBot", mc)
        self.agents = ["insultbot", "anotherbot"]

    async def send_message_async(self, message):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.send_message, message)

    async def greet(self):
        await self.send_message_async("Hello, I'm your reflective bot")

    async def bye(self):
        await self.send_message_async("Bye, see you next time!")

    async def help(self):
        await self.send_message_async(
            "Available commands: greet, help, joke, bye, place_block"
        )

    async def joke(self):
        await self.send_message_async("joke joke joke.")

    async def place_block(self):
        pos = self.mc.player.getTilePos()
        self.mc.setBlock(pos.x, pos.y - 1, pos.z, block.DIAMOND_BLOCK.id)
        await self.send_message_async("Placed a diamond block under your feet!")

    def __getattr__(self, attr):
        async def unknown_command(*args, **kwargs):
            await self.send_message_async(f"Unknown method or command '{attr}'")
        return unknown_command

    async def perform_task(self, stop_event):
        await self.send_message_async("ReflectiveBot is active. You can interrupt me using 'stop' command.")
        await self.help()

        try:
            while not stop_event.is_set():
                chat_events = self.mc.events.pollChatPosts()
                for event in chat_events:
                    if message == "stop":
                        stop_event.set()
                        return
                    message = event.message.strip().lower()
                    if message.startswith("reflective "):
                        command = message.split("reflective ")[1]
                        await self.respond(command)
                    elif message in self.agents:
                        stop_event.set()
                        await self.send_message_async(f"Stopping ReflectiveBot and switching to {message}.")
                        return
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            await self.send_message_async("ReflectiveBot has been forcefully stopped.")
        finally:
            await self.send_message_async("ReflectiveBot has been interrupted.")

    async def respond(self, command):
        if hasattr(self, command):
            method = getattr(self, command)
        else:
            await self.send_message_async(f"Unknown command: {command}")