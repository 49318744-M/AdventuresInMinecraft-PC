import time
from mcpi import minecraft

class MinecraftAgent:
    def __init__(self, name, mc):
        self.name = name
        self.mc = mc  # Use the provided Minecraft instance

    def perform_task(self, stop_event):
        """Defines the task to be performed by the agent. Supports interruption."""
        while not stop_event.is_set():  # Check for stop event to interrupt the task
            self.send_message(f"{self.name} is performing its task.")
            time.sleep(5)  # Simulate performing a task

        self.send_message(f"{self.name} has been interrupted.")

    def send_message(self, message):
        """Sends a message in the Minecraft world."""
        self.mc.postToChat(f"{self.name}: {message}")

    def get_position(self):
        """Returns the current position of the player."""
        return self.mc.player.getTilePos()
    
    def set_block(self, x, y, z, block):
        """Sets the block at the specified position."""
        self.mc.setBlock(x, y, z, block)