# https://github.com/DataDog/datadogpy
# https://github.com/py3minepi/py3minepi

import mcpi.minecraft as minecraft
import render
import fetch

# mc=minecraft.Minecraft.create()
# mc.postToChat("hello world")

if __name__ == '__main__':
    mc = minecraft.Minecraft.create()
    render.draw_simple_wall(mc, (2,2,2), (0,100), fetch.get_simple_data('http://...', 'foo', 'bar', 'ohwhatshouldweputhere'))
