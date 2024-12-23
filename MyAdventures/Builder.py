import time
import mcpi.minecraft as minecraft
import mcpi.block as block

class Builder:
    def __init__(self, mc):
        self.mc = mc

    def build_wall(self, x, y, z, length, height, block_id, direction='x'):
        raise NotImplementedError()

    def build_column(self, x, y, z, height, block_id):
        raise NotImplementedError()

    def build_window(self, x, y, z, width, height):
        raise NotImplementedError()
    
    def build_roof(self, x, y, z, width, depth, height, block_id):
        raise NotImplementedError()

    def build_filler(self, x, y, z, width, height, block_id):
        raise NotImplementedError()

    def build_door(self, x, y, z):
        raise NotImplementedError()

    def add_decorations(self, x, y, z, house_width, house_depth, house_height):
        raise NotImplementedError()

    def build_stairs(self, x, y, z, direction='z'):
        raise NotImplementedError()

 