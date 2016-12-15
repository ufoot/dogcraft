# https://github.com/DataDog/datadogpy
# https://github.com/py3minepi/py3minepi

import mcpi.minecraft as minecraft
import render
import fetch
import math
import time
# mc=minecraft.Minecraft.create()
# mc.postToChat("hello world")

if __name__ == '__main__':
    mc = minecraft.Minecraft.create("172.86.162.69")
    # render.draw_simple_wall(mc, (2,2,2), (0,100), fetch.get_simple_data('http://...', 'foo', 'bar', 'ohwhatshouldweputhere'))

    def function(x):
        return math.sin(x*6)**2
    points = [function(x) for x in range(30)]
    i = 30
    render.draw_status_check(mc, (-30, 47, 80), 1, render.STATUS_ERROR)
    render.draw_status_check(mc, (-22, 47, 80), 1, render.STATUS_OK)
    render.draw_status_check(mc, (-14, 47, 80), 1, render.STATUS_WARNING)


    while True:
        i += 1
        time.sleep(1)
        points = points[1:]
        points.append(function(i))
        render.draw_simple_wall(mc, (-30, 47, 70), (50, 15), points)
