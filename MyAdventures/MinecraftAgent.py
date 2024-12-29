from abc import ABC, abstractmethod
from mcpi.minecraft import Minecraft

class MinecraftAgent(ABC):
    def __init__(self, name):
        self.name = name
        self.mc = Minecraft.create()  # Connect to Minecraft
        self.position = self.mc.player.getTilePos()  # Get player's current position
    
    def move(self, x, y, z):
        """Moves the agent to a specific position."""
        self.mc.player.setTilePos(x, y, z)
    
    def send_message(self, message):
        """Sends a message in the Minecraft world."""
        self.mc.postToChat(f"{self.name}: {message}")
    
    def get_position(self):
        """Returns the current position of the agent."""
        return self.mc.player.getTilePos()

    @abstractmethod
    def perform_task(self):
        """Defines the task to be performed by the agent."""
        pass
