from math import floor
import mcpi.block as block

def draw_simple_wall(mc, pos, size, data):
    """Render a single line of data as a wall"""
    x, y, z = pos
    w, h = size
    for i, value in enumerate(data):
        blocks_to_display = floor(h * value)
        # Display dirt
        for j in range(blocks_to_display):
            mc.setBlock(x + i, y + j, z, block.STONE.id)
        # Clean the top
        for k in range(blocks_to_display, h):
            mc.setBlock(x + i, y + k, z, 0)
