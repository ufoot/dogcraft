from math import floor
import mcpi.block as block

STATUS_OK = "ok"
STATUS_WARNING = "warning"
STATUS_ERROR = "error"

WOOL_GREEN_DATA = 13
WOOL_RED_DATA = 14
WOOL_ORANGE_DATA = 1

ok_message = [(0,0), (0, 1), (0, 2), (0, 3), (1,3), (2, 3), (2, 2), (2,1), (2, 0), (1, 0)]


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


def draw_status_check(mc, pos, size, status):
    x, y, z = pos
    block_data = WOOL_GREEN_DATA
    message = ok_message
    if status == STATUS_OK:
        block_data = WOOL_GREEN_DATA
        message = ok_message
    elif status == STATUS_ERROR:
        block_data = WOOL_RED_DATA
        # TODO error message
    elif status == STATUS_WARNING:
        block_data = WOOL_ORANGE_DATA
        # TODO warning message

    for x_i in range(7):
        for y_i in range(6):
            mc.setBlock(x + x_i, y + y_i, z, block.WOOL.id, block_data)

    for (x_i, y_i) in message:
        mc.setBlock(x + 2 + x_i, y + 1 +  y_i, z, block.WOOL.id, 0) # Blank message
