#InsultBot

import mcpi.minecraft as minecraft
import random
import time

# Connect to Minecraft 
mc = minecraft.Minecraft.create()

# List of insults
insults = [
    "Do you even know how to play?",
    "You're slower than a turtle!",
    "You're a total m***",
    "You can't even build a house!",
    "You're acting s***",
    "You really are a c***",
    "You're a disaster!"
]
# Shuffle the list of insults
random.shuffle(insults)

while True:
    for insult in insults:
        mc.postToChat(insult)
        time.sleep(10)  # Wait 10 seconds before sending the next insult

    # Reshuffle the list after all insults have been used
    random.shuffle(insults)
