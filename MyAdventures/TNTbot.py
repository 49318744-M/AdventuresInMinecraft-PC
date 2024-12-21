#TNTbot
import mcpi.minecraft as minecraft
import mcpi.block as block
import time

# Connect to the Minecraft game
mc = minecraft.Minecraft.create()

while True:
    pos = mc.player.getTilePos()  # Get the player's position
    mc.setBlock(pos.x, pos.y, pos.z, block.TNT, 1)  # Place TNT
    time.sleep(1)  # Wait a second

    # Ignite the TNT by placing fire next to it
    mc.setBlock(pos.x, pos.y, pos.z + 1, block.FIRE)  # Place fire next to the TNT
    mc.postToChat("Boom!")
    
    time.sleep(3)  # Wait for the explosion to happen
    time.sleep(5)  # Wait 5 seconds before the next explosion
