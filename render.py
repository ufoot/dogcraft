from math import floor
import mcpi.block as block


"""
TODOS
- draw a line around graph ?
- draw a whole dashboard with several graphs
- draw only values that change
"""
STATUS_OK = "ok"
STATUS_WARNING = "warning"
STATUS_ERROR = "error"

WOOL_GREEN_DATA = 13
WOOL_RED_DATA = 14
WOOL_ORANGE_DATA = 1

FILLED = block.STONE.id
BORDER = block.SANDSTONE.id

ok_message = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3),
              (2, 3), (2, 2), (2, 1), (2, 0), (1, 0)]
error_message = [(0, 0), (1, 1), (1, 2), (0, 3), (2, 3), (2, 0), (2, 0)]
warning_message = [(-1, 1), (-1, 2), (0, 0), (1, 1), (2, 0), (3, 1), (3, 2)]


def draw_simple_wall(mc, pos, size, data):
    """Render a single line of data as a wall"""
    x, y, z = pos
    w, h = size
    for i, value in enumerate(data):
        blocks_to_display = floor(h * value)
        # Display filled
        for j in range(blocks_to_display):
            mc.setBlock(x + i, y + j, z, FILLED)
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
        message = error_message
    elif status == STATUS_WARNING:
        block_data = WOOL_ORANGE_DATA
        message = warning_message

    for x_i in range(7):
        for y_i in range(6):
            mc.setBlock(x + x_i, y + y_i, z, block.WOOL.id, block_data)

    for (x_i, y_i) in message:
        mc.setBlock(x + 2 + x_i, y + 1 + y_i, z,
                    block.WOOL.id, 0)  # Blank message


# TODO: write unit test for this, this could become a nigthmare...
_transfos = {"xy": [lambda p: p, lambda p: p],
             "yz": [lambda p: (p[1], p[2], p[0]), lambda p: (p[2], p[0], p[1])],
             "zy": [lambda p: (p[2], p[1], p[0]), lambda p: (p[2], p[1], p[0])],
             "xz": [lambda p: (p[0], p[2], p[1]), lambda p: (p[0], p[2], p[1])],
             "yx": [lambda p: (p[1], p[0], p[2]), lambda p: (p[1], p[0], p[2])],
             "zx": [lambda p: (p[2], p[0], p[1]), lambda p: (p[1], p[2], p[0])],
             }


def draw_flat_wall(mc=None, pos1=(0, 0, 0), pos2=(10, 10, 0), layout="xy", border=True, data=[]):
    """Render a single line of data as a wall"""

    abctoxyz, xyztoabc = _transfos[layout]

    x1, y1, z1 = abctoxyz(pos1)
    x2, y2, z2 = abctoxyz(pos2)

    if x1 == x2:
        return  # too thin
    if y1 == y2:
        return  # too thin
    if len(data) == 0:
        return  # no data
    z = (z1 + z2) / 2

    r = range(x1, x2) if (x1 < x2) else range(x2 + 1, x1 + 1)

    for x in r:
        i = int(floor((float(x - x1) / float(x2 - x1)) * len(data)))
        v = int(floor(data[i] * y2 + (1.0 - data[i]) * y1))
        rfilled = range(y1, v) if (y1 < y2) else range(v + 1, y1 + 1)
        rclean = range(v, y2) if (y1 < y2) else range(y2 + 1, v + 1)
        # Display filled
        for y in rfilled:
            a, b, c = xyztoabc((x, y, z))
            if border and (x == x1 or abs(x2 - x) <= 1 or y == y1 or abs(y2 - y) <= 1):
                # Display border
                mc.setBlock(a, b, c, BORDER)
            else:
                mc.setBlock(a, b, c, FILLED)
        # Clean the top
        for y in rclean:
            a, b, c = xyztoabc((x, y, z))
            if border and (x == x1 or abs(x2 - x) <= 1 or y == y1 or abs(y2 - y) <= 1):
                # Display border
                mc.setBlock(a, b, c, BORDER)
            else:
                mc.setBlock(a, b, c, 0)


def erase_flat_wall(mc=None, pos1=(0, 0, 0), pos2=(10, 10, 0), layout="xy", border=True, data=[]):
    """Erases everything where a wall was"""

    abctoxyz, xyztoabc = _transfos[layout]

    x1, y1, z1 = abctoxyz(pos1)
    x2, y2, z2 = abctoxyz(pos2)

    if x1 == x2:
        return  # too thin
    if y1 == y2:
        return  # too thin
    z = (z1 + z2) / 2

    r = range(x1, x2) if (x1 < x2) else range(x2 + 1, x1 + 1)
    for x in r:
        rsub = range(y1, y2) if (y1 < y2) else range(y2 + 1, y1 + 1)
        # Clean
        for y in rsub:
            a, b, c = xyztoabc((x, y, z))
            mc.setBlock(a, b, c, 0)
