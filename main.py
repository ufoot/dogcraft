# https://github.com/DataDog/datadogpy
# https://github.com/py3minepi/py3minepi

import mcpi.minecraft as minecraft
import render
import fetch
from dashboard import Dashboard
import math
import time
import sys
from cleanup import set_cleanup_callback

# mc=minecraft.Minecraft.create()
# mc.postToChat("hello world")

if __name__ == '__main__':
    fetch.initialize()
    mc = minecraft.Minecraft.create("172.86.162.69")
    dashboards = []

    # Load dashboards
    for arg in sys.argv[1:]:
        dashboards.append(Dashboard(arg, mc))

    set_cleanup_callback(lambda: [dashboard.cleanup()
                                  for dashboard in dashboards])

    # Run the update every n seconds
    while True:
        print("drawing %d dashboard(s)" % len(dashboards))
        for dashboard in dashboards:
            dashboard.update()
        time.sleep(1)
