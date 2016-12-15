# https://github.com/DataDog/datadogpy
# https://github.com/py3minepi/py3minepi

import mcpi.minecraft as minecraft
import render
import fetch
from dashboard import Dashboard
import math
import time
import sys

# mc=minecraft.Minecraft.create()
# mc.postToChat("hello world")

if __name__ == '__main__':
    fetch.initialize()
    mc = minecraft.Minecraft.create("172.86.162.69")
    dashboards = []

    # Load dashboards
    for arg in sys.argv[1:]:
        dashboards.append(Dashboard(arg, mc))

    # Run the update every n seconds
    while True:
        time.sleep(0.5)
        for dashboard in dashboards:
            dashboard.update()
        # TODO: get rid of this once dashboards work
        points = fetch.get_demo_data()
        # print(points)
        render.draw_flat_wall(
            mc=mc, pos1=(-30, 30, 75), pos2=(20, 45, 75), layout="xy", border=True, data=points)
        render.draw_flat_wall(
            mc=mc, pos1=(-30, 30, 90), pos2=(20, 30, 75), layout="xz", border=True, data=points)
