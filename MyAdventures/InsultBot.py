import random
import time
from MinecraftAgent import MinecraftAgent

class InsultBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("InsultBot", mc)
        self.insults = [
            "Do you even know how to play?",
            "You're slower than a turtle!",
            "You're a total m***",
            "You can't even build a house!",
            "You're acting s***",
            "You really are a c***",
            "You're a disaster!"
        ]
        random.shuffle(self.insults)

    def perform_task(self, stop_event):
        for insult in self.insults:
            if stop_event.is_set():  # Check if the task should be stopped
                self.send_message(f"{self.name} has been interrupted.")
                break
            self.send_message(insult)
            time.sleep(5)  # Wait before sending the next insult
        random.shuffle(self.insults)

