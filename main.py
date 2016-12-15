# https://github.com/DataDog/datadogpy
# https://github.com/py3minepi/py3minepi

import mcpi.minecraft as minecraft
import render
import fetch
import math
# mc=minecraft.Minecraft.create()
# mc.postToChat("hello world")

if __name__ == '__main__':
    mc = minecraft.Minecraft.create("172.86.162.69")
    # render.draw_simple_wall(mc, (2,2,2), (0,100), fetch.get_simple_data('http://...', 'foo', 'bar', 'ohwhatshouldweputhere'))
    render.draw_simple_wall(mc, (-10, 47, 52), (50, 10), [(math.sin(x*6))**2 for x in range(100)])
