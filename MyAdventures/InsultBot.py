#InsultBot
import random
import time
from MinecraftAgent import MinecraftAgent

class InsultBot(MinecraftAgent):
    def __init__(self):
        super().__init__("InsultBot")
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

    def perform_task(self):
        """Send a set of insults one by one."""
        for insult in self.insults:
            self.send_message(insult)
            time.sleep(10)  # Wait 10 seconds before sending the next insult

        self.send_message("Insults completed!")  # Inform that the task is finished
