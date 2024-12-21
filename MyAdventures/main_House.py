import time
from House import BuildDestroy
import mcpi.minecraft as minecraft

if __name__ == "__main__":
    mc = minecraft.Minecraft.create()
    bot = BuildDestroy(mc)

    # Player's current position
    pos = mc.player.getTilePos()

    # Coordinates where the house will be built
    offset_x = pos.x + 5
    offset_z = pos.z

    # House dimensions
    house_width = 11
    house_depth = 10
    house_height = 7
    roof_height = 5

    # Build the house
    bot.build_house(offset_x, pos.y, offset_z, house_width, house_depth, house_height, roof_height)

    # Wait 10 seconds before starting the destruction
    time.sleep(10)

    # Destroy the house
    bot.destroy_house(offset_x, pos.y, offset_z, house_width, house_depth, house_height, roof_height)
