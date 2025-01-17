import inspect
import threading
import time
from MinecraftAgent import MinecraftAgent
from mcpi import minecraft

class ReflectiveBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("ReflectiveBot", mc)

    def greet(self):
        self.mc.postToChat(f"Hello Im your reflective bot")

    def bye(self):
        self.mc.postToChat(f"BYYE")

    def help(self):
        self.mc.postToChat(
            "Available commands: greet, help, joke, bye\n"
        )

    def joke(self):
        self.mc.postToChat("joke")

    def __getattr__(self, attr):
        return lambda *args, **kwargs: self.mc.postToChat(
            f"Method or atribute '{attr}' undefined, but called dynamically."
        )

    def respond(self, command):
        if hasattr(self, command):
            getattr(self, command)() 
        else:
            self.mc.postToChat(f"Unknown command: {command}")