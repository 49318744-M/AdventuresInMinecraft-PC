import mcpi.minecraft as minecraft
from BuildHouse import BuildHouse
import time

import mcpi.minecraft as minecraft

if __name__ == "__main__":
    mc = minecraft.Minecraft.create()
    bot = BuildHouse(mc)

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
    # Build walls
    bot.build_wall(offset_x, pos.y, offset_z, house_width, house_height, 98, direction='x')
    bot.build_wall(offset_x, pos.y, offset_z, house_depth, house_height, 98, direction='z')
    bot.build_wall(offset_x, pos.y, offset_z + house_depth, house_width, house_height, 98, direction='x')
    bot.build_wall(offset_x + house_width - 1, pos.y, offset_z, house_depth, house_height, 98, direction='z')

    # Build columns at the 4 corners in pink (id: 201)
    bot.build_column(offset_x, pos.y, offset_z, house_height, 201)
    bot.build_column(offset_x + house_width - 1, pos.y, offset_z, house_height, 201)
    bot.build_column(offset_x, pos.y, offset_z + house_depth, house_height, 201)
    bot.build_column(offset_x + house_width - 1, pos.y, offset_z + house_depth, house_height, 201)

    # Add windows
    bot.build_window(offset_x, pos.y + 2, offset_z + 2, 3, 3)
    bot.build_window(offset_x, pos.y + 2, offset_z + house_depth - 4, 3, 3)
    bot.build_window(offset_x + 4 + house_width - 5, pos.y + 2, offset_z + 2, 3, 3)
    bot.build_window(offset_x + 4 + house_width - 5, pos.y + 2, offset_z + house_depth - 4, 3, 3)

    # Build filler between the wall and the roof
    bot.build_filler(offset_x, pos.y + house_height, offset_z, house_width, roof_height - 1, 98)
    bot.build_filler(offset_x, pos.y + house_height, offset_z + house_depth, house_width, roof_height - 1, 98)

    # Build the roof
    bot.build_roof(offset_x, pos.y + house_height, offset_z - 1, house_width, house_depth + 3, roof_height, 17)

        # Build door
    bot.build_door(offset_x + 5, pos.y + 2, offset_z)

        # Add decorations
    bot.add_decorations(offset_x, pos.y, offset_z, house_width, house_depth, house_height)

        # Build stairs
    bot.build_stairs(offset_x + 5, pos.y, offset_z - 1, direction='z')  
    bot.build_stairs(offset_x + 4, pos.y, offset_z - 1, direction='z')  
    bot.build_stairs(offset_z + 6, pos.y, offset_z - 1, direction='z')  

    # Wait 10 seconds before starting the destruction
    time.sleep(10)

    # Destroy the house
    # Destroy stairs
    bot.destroy_stairs(offset_x + 5, pos.y, offset_z - 1)
    bot.destroy_stairs(offset_x + 4, pos.y, offset_z - 1)
    bot.destroy_stairs(offset_x + 6, pos.y, offset_z - 1)

    # Destroy decorations
    bot.destroy_decorations(offset_x, pos.y, offset_z, house_width, house_depth, house_height)

    # Destroy door
    bot.destroy_door(offset_x + 5, pos.y + 2, offset_z)

    # Destroy roof
    bot.destroy_roof(offset_x, pos.y + house_height, offset_z - 1, house_width, house_depth + 3, roof_height)

    # Destroy filler between the wall and the roof
    bot.destroy_filler(offset_x, pos.y + house_height, offset_z, house_width, roof_height - 1)
    bot.destroy_filler(offset_x, pos.y + house_height, offset_z + house_depth, house_width, roof_height - 1)

    # Destroy windows
    bot.destroy_window(offset_x, pos.y + 2, offset_z + 2, 3, 3)
    bot.destroy_window(offset_x, pos.y + 2, offset_z + house_depth - 4, 3, 3)
    bot.destroy_window(offset_x + 4 + house_width - 5, pos.y + 2, offset_z + 2, 3, 3)
    bot.destroy_window(offset_x + 4 + house_width - 5, pos.y + 2, offset_z + house_depth - 4, 3, 3)

    # Destroy columns at the 4 corners
    bot.destroy_column(offset_x, pos.y, offset_z, house_height)
    bot.destroy_column(offset_x + house_width - 1, pos.y, offset_z, house_height)
    bot.destroy_column(offset_x, pos.y, offset_z + house_depth, house_height)
    bot.destroy_column(offset_x + house_width - 1, pos.y, offset_z + house_depth, house_height)

    # Destroy walls
    bot.destroy_wall(offset_x, pos.y, offset_z, house_width, house_height, direction='x')
    bot.destroy_wall(offset_x, pos.y, offset_z, house_depth, house_height, direction='z')
    bot.destroy_wall(offset_x, pos.y, offset_z + house_depth, house_width, house_height, direction='x')
    bot.destroy_wall(offset_x + house_width - 1, pos.y, offset_z, house_depth, house_height, direction='z')