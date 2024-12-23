# Program that performs basic instructions

import mcpi.minecraft as minecraft
mc = minecraft.Minecraft.create()

# Send a message to the game chat
mc.postToChat("Hello world")

# Print the player's position in the shell
pos = mc.player.getTilePos()
print(f"Your position is: x={pos.x}, y={pos.y}, z={pos.z}")

# Place a block 2 positions in front of the player
mc.setBlock(pos.x, pos.y, pos.z - 2, 1)

# Create a 3x3x3 cube of dirt (ID 3) at the player's position
for x in range(3):
    for y in range(3):
        for z in range(3):
            mc.setBlock(pos.x + x, pos.y + y, pos.z + z, 3)

# Create a tower of gold blocks under the player
for i in range(10):  # Tower height of 10 blocks
    mc.setBlock(pos.x, pos.y + i, pos.z, 41)  # 41 is the ID for gold

# Detect player block hits
events = mc.events.pollBlockHits()
for event in events:
    print(f"You hit a block at x={event.pos.x}, y={event.pos.y}, z={event.pos.z}!")
