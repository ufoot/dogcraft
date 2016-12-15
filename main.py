# https://github.com/DataDog/datadogpy
# https://github.com/py3minepi/py3minepi

import mcpi.minecraft as minecraft
import render
import fetch

# mc=minecraft.Minecraft.create()
# mc.postToChat("hello world")

if __name__ == '__main__':
    fetch.initialize()
    mc = minecraft.Minecraft.create()
    render.draw_simple_wall(mc, (2, 2, 2), (0, 100), fetch.get_simple_data(
        query='sum:kafka.consumer_lag{consumer_group:smelter}', delay=300))
