import mcpi.minecraft as minecraft
from BuildBridge import BuildBridge
import time
if __name__ == "__main__":
    mc = minecraft.Minecraft.create()  # Connect to the Minecraft server
    
    # Define the parameters for the bridge 
    length = 20  # Length of the bridge
    width = 5    # Width of the bridge
    height = 3   # Height of the bridge (for stairs and support)
    material = 5  # Material (5 corresponds to wood planks)
    stair_type = 0  # Stair type (0 for one direction, 1 for the other)

    # Create an instance of BuildBridge
    bot = BuildBridge(mc, length, width, height, material, stair_type)

    # Player's initial position
    pos = mc.player.getTilePos()

    # Coordinates for starting the bridge
    x = pos.x + 5
    y = pos.y
    z = pos.z

    # BUILD the bridge
    print("Starting the bridge construction!")
    for w in range(width):
        bot.build_wall(x, y, z + w, length, 1, material)

    # Build side walls
    bot.build_wall(x, y - 1, z, length, 1, material)
    bot.build_wall(x, y - 1, z + width - 1, length, 1, material)

    # Create the barriers 
    bot.build_barriers(x, y, z, length, width)

    # Build the supports of the bridge
    bot.build_feet(x, y, z, length, width, material)

    for w in range(width):
        # Build stairs at the front side 
        bot.build_stairs(x - 3, y - 3, z + w, height, 'x', stair_type)
        # Build stairs at the other side 
        bot.build_stairs(x + length + 2, y - 3, z + w, height, 'y', stair_type)

    print("Bridge constructed!")