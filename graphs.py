import os
from fetch import get_simple_data, get_demo_data, DEFAULT_DELAY
from render import draw_flat_wall, erase_flat_wall, WOOL, WOOL_RED_DATA, DEFAULT_TITLE
import fetch
import render
import random
import os

DEFAULT_FILLED_COLOR = 'light_blue'
DEFAULT_BORDER_COLOR = 'yellow'


class AbstractGraph(object):

    def __init__(self, graph_conf, mc):
        self.pos1 = (graph_conf['pos1']['x'], graph_conf[
                     'pos1']['y'], graph_conf['pos1']['z'])
        self.pos2 = (graph_conf['pos2']['x'], graph_conf[
                     'pos2']['y'], graph_conf['pos2']['z'])
        self.query = graph_conf['query']
        self.layout = graph_conf['layout'] if 'layout' in graph_conf else "xy"
        self.title = graph_conf[
            'title'] if 'title' in graph_conf else DEFAULT_TITLE
        self.delay = graph_conf[
            'delay'] if 'delay' in graph_conf else DEFAULT_DELAY
        self.border = graph_conf['border'] if 'border' in graph_conf else False
        self.filled_data = render.COLORS[graph_conf[
            'filled_color'] if 'filled_color' in graph_conf else DEFAULT_FILLED_COLOR]
        self.border_data = render.COLORS[graph_conf[
            'border_color'] if 'border_color' in graph_conf else DEFAULT_BORDER_COLOR]
        self.mc = mc

    def update(self):
        raise Exception("Not implemented")

    def cleanup(self):
        raise Exception("Not implemented")

    def get_data(self):
        if os.environ.get('DATADOG_DEMO_DATA'):
            return get_demo_data()
        return get_simple_data(query=self.query, delay=self.delay)


class Wall(AbstractGraph):

    def update(self):
        data = self.get_data()
        draw_flat_wall(mc=self.mc, pos1=self.pos1, pos2=self.pos2,
                       layout=self.layout, title=self.title,
                       border=self.border, data=data,
                       filled_data=self.filled_data,
                       border_data=self.border_data)
        pass

    def cleanup(self):
        erase_flat_wall(mc=self.mc, pos1=self.pos1, pos2=self.pos2,
                        layout=self.layout)
        pass


class Mountain(AbstractGraph):

    def update(self):
        data = self.get_data()
        self.mc.postToChat("Updating montain")
        pass

    def cleanup(self):
        pass


class StatusCheck(AbstractGraph):

    def update(self):
        data = self.get_data()
        # TODO Call the display function
        pass

    def cleanup(self):
        pass


class MonitorStatus(AbstractGraph):

    def __init__(self, graph_conf, mc):
        self.pos1 = (graph_conf['pos1']['x'], graph_conf[
                     'pos1']['y'], graph_conf['pos1']['z'])
        self.pos2 = (graph_conf['pos2']['x'], graph_conf[
                     'pos2']['y'], graph_conf['pos2']['z'])

        self.monitor_id = graph_conf['monitor_id']
        self.layout = graph_conf['layout'] if 'layout' in graph_conf else "xy"
        self.title = graph_conf[
            'title'] if 'title' in graph_conf else DEFAULT_TITLE
        self.mc = mc
        self.blink = False

    def update(self):
        if os.environ.get('DATADOG_DEMO_DATA'):
            data = random.choice([fetch.MONITOR_STATUS_OK,
                                  fetch.MONITOR_STATUS_WARN, fetch.MONITOR_STATUS_ALERT])
        else:
            data = fetch.get_monitor_status(self.monitor_id)

        if data == fetch.MONITOR_STATUS_OK:
            block_color = render.COLORS['green']
        elif data == fetch.MONITOR_STATUS_ALERT:
            # blink on alert, to catch your eye
            if self.blink:
                block_color = render.COLORS['black']
            else:
                block_color = render.COLORS['red']
            self.blink = not self.blink
        elif data == fetch.MONITOR_STATUS_WARN:
            block_color = render.COLORS['orange']
        elif data == fetch.MONITOR_STATUS_NO_DATA:
            block_color = render.COLORS['grey']

        draw_flat_wall(mc=self.mc, pos1=self.pos1, pos2=self.pos2, layout=self.layout, title=self.title,
                       border=False, data=[1.0],
                       filled_data=block_color)

    def cleanup(self):
        erase_flat_wall(mc=self.mc, pos1=self.pos1, pos2=self.pos2,
                        layout=self.layout)


TYPES = {
    'wall': Wall,
    'mountain': Mountain,
    "status_check": StatusCheck,
    "monitor_status": MonitorStatus,
}
