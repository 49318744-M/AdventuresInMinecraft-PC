import time
import mcpi.minecraft as minecraft
import mcpi.block as block
from MinecraftAgent import MinecraftAgent
import asyncio

class BuildHouse(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("BuildHouse", mc)

    def build_wall(self, x, y, z, length, height, block_id, direction='x'):
        for i in range(length):
            for j in range(height):
                self.mc.setBlock(x + i if direction == 'x' else x,
                                 y + j,
                                 z if direction == 'x' else z + i,
                                 block_id)
                time.sleep(0.05)

    def build_column(self, x, y, z, height, block_id):
        for j in range(height):
            self.mc.setBlock(x, y + j, z, block_id)
            time.sleep(0.05)

    def build_window(self, x, y, z, width, height):
        for i in range(width):
            for j in range(height):
                self.mc.setBlock(x, y + j, z + i, 102)  # Glass block (id 102)
                time.sleep(0.05)

    def build_roof(self, x, y, z, width, depth, height, block_id):
        for i in range(height): 
            for j in range(depth):
                self.mc.setBlock(x + i, y + i, z + j, block_id)
                self.mc.setBlock(x + i - 1, y + i, z + j, block_id)
                time.sleep(0.05)
                self.mc.setBlock(x + width - i - 1, y + i, z + j, block_id)
                self.mc.setBlock(x + width - i, y + i, z + j, block_id)
                time.sleep(0.05)

        # Add the last line at the top of the roof
        for j in range(depth):
            self.mc.setBlock(x + width // 2, y + height - 1, z + j, block_id)
            time.sleep(0.05)

    def build_filler(self, x, y, z, width, height, block_id):
        for i in range(height):
            for j in range(width - 2 * i):
                self.mc.setBlock(x + i + j, y + i, z, block_id)
                time.sleep(0.05)

    def build_door(self, x, y, z): 
        self.mc.setBlock(x, y - 1, z, 0)  # Clear space for the door (1x2)
        self.mc.setBlock(x, y, z, 0)  
        self.mc.setBlock(x, y - 1, z, 64, 0)   # Place the door
        self.mc.setBlock(x, y, z, 64, 8) # Door block id
        time.sleep(0.05)

    def add_decorations(self, x, y, z, house_width, house_depth, house_height):
        flower_height = y + 2
        self.mc.setBlock(x + 3, flower_height, z, 38)  # Flower (id 38)
        self.mc.setBlock(x + 7, flower_height, z, 38)
        time.sleep(0.05)
        
        lantern_height = y + house_height - 1
        self.mc.setBlock(x + 2, lantern_height, z, 50)  # Lanterns (id 50)
        self.mc.setBlock(x + 8, lantern_height, z, 50)
        time.sleep(0.05)

        # Windows
        self.mc.setBlock(x + 5, y + 7, z, 102)  # Glass block(id 102)
        self.mc.setBlock(x + 5, y + 6, z, 102)
        self.mc.setBlock(x + 4, y + 7, z, 102)
        self.mc.setBlock(x + 4, y + 6, z, 102)
        self.mc.setBlock(x + 6, y + 7, z, 102)
        self.mc.setBlock(x + 6, y + 6, z, 102)
        time.sleep(0.05)

    def build_stairs(self, x, y, z, direction='z'):
        self.mc.setBlock(x, y, z, 53, 2)  # Stairs (id 53)
        time.sleep(0.05)

    async def perform_task(self, stop_event):
        try:
            pos = self.mc.player.getTilePos()
            print(f"Posición del jugador: x={pos.x}, y={pos.y}, z={pos.z}")
        except Exception as e:
            self.send_message(f"Error al obtener la posición del jugador: {e}")
            return

        offset_x = pos.x + 5
        offset_z = pos.z

        # Dimensions of the house
        house_width = 11
        house_depth = 10
        house_height = 7
        roof_height = 5

        # Walls
        for task in [
            lambda: self.build_wall(offset_x, pos.y, offset_z, house_width, house_height, 98, direction='x'),
            lambda: self.build_wall(offset_x, pos.y, offset_z, house_depth, house_height, 98, direction='z'),
            lambda: self.build_wall(offset_x, pos.y, offset_z + house_depth, house_width, house_height, 98, direction='x'),
            lambda: self.build_wall(offset_x + house_width - 1, pos.y, offset_z, house_depth, house_height, 98, direction='z'),
        ]:
            if stop_event.is_set():  # Verifica si la tarea debe interrumpirse
                self.send_message("Construcción interrumpida.")
                return
            task()

        # Columns
        for task in [
            lambda: self.build_column(offset_x, pos.y, offset_z, house_height, 201),
            lambda: self.build_column(offset_x + house_width - 1, pos.y, offset_z, house_height, 201),
            lambda: self.build_column(offset_x, pos.y, offset_z + house_depth, house_height, 201),
            lambda: self.build_column(offset_x + house_width - 1, pos.y, offset_z + house_depth, house_height, 201),
        ]:
            if stop_event.is_set():
                self.send_message("Construcción interrumpida.")
                return
            task()

        # Windows
        for task in [
            lambda: self.build_window(offset_x, pos.y + 2, offset_z + 2, 3, 3),
            lambda: self.build_window(offset_x, pos.y + 2, offset_z + house_depth - 4, 3, 3),
            lambda: self.build_window(offset_x + 4 + house_width - 5, pos.y + 2, offset_z + 2, 3, 3),
            lambda: self.build_window(offset_x + 4 + house_width - 5, pos.y + 2, offset_z + house_depth - 4, 3, 3),
        ]:
            if stop_event.is_set():
                self.send_message("Construcción interrumpida.")
                return
            task()
        
        # Filler
        if not stop_event.is_set():
            self.build_filler(offset_x, pos.y + house_height, offset_z, house_width, roof_height - 1, 98)
            self.build_filler(offset_x, pos.y + house_height, offset_z + house_depth, house_width, roof_height - 1, 98)

        # Roof
        if not stop_event.is_set():
            self.build_roof(offset_x, pos.y + house_height, offset_z - 1, house_width, house_depth + 3, roof_height, 17)

        # Door
        if not stop_event.is_set():
            self.build_door(offset_x + 5, pos.y + 2, offset_z)

        # Decorations
        if not stop_event.is_set():
            self.add_decorations(offset_x, pos.y, offset_z, house_width, house_depth, house_height)

        # Stairs
        if not stop_event.is_set():
            self.build_stairs(offset_x + 5, pos.y, offset_z - 1, direction='z')
            self.build_stairs(offset_x + 4, pos.y, offset_z - 1, direction='z')
            self.build_stairs(offset_z + 6, pos.y, offset_z - 1, direction='z')
        await asyncio.sleep(1)