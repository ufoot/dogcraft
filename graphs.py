from fetch import get_simple_data, get_demo_data
from render import draw_flat_wall, WOOL, WOOL_RED_DATA
import fetch
import render

class AbstractGraph(object):

    def __init__(self, graph_conf, mc):
        self.pos1 = (graph_conf['pos1']['x'], graph_conf[
                     'pos1']['y'], graph_conf['pos1']['z'])
        self.pos2 = (graph_conf['pos2']['x'], graph_conf[
                     'pos2']['y'], graph_conf['pos2']['z'])
        self.query = graph_conf['query']
        self.layout = graph_conf['layout'] if 'layout' in graph_conf else "xy"
        self.border = graph_conf['border'] if 'border' in graph_conf else false
        self.mc = mc

    def update(self):
        raise Exception("Not implemented")

    def get_data(self):
        # return get_simple_data(self.query)
        return get_demo_data()


class Wall(AbstractGraph):

    def update(self):
        data = self.get_data()
        draw_flat_wall(mc=self.mc, pos1=self.pos1, pos2=self.pos2,
                       layout=self.layout, border=self.border, data=data)
        pass


class Mountain(AbstractGraph):

    def update(self):
        data = self.get_data()
        self.mc.postToChat("Updating montain")
        pass


class StatusCheck(AbstractGraph):

    def update(self):
        data = self.get_data()
        # TODO Call the display function
        pass


class MonitorStatus(AbstractGraph):

    def __init__(self, graph_conf, mc):
        self.pos1 = (graph_conf['pos1']['x'], graph_conf[
                     'pos1']['y'], graph_conf['pos1']['z'])
        self.pos2 = (graph_conf['pos2']['x'], graph_conf[
                     'pos2']['y'], graph_conf['pos2']['z'])

        self.monitor_id = graph_conf['monitor_id']
        self.layout = graph_conf['layout'] if 'layout' in graph_conf else "xy"
        self.mc = mc


    def update(self):
        data = fetch.get_monitor_status(self.monitor_id)
        if data == fetch.MONITOR_STATUS_OK:
            block_color = render.COLORS['green']
        elif data == fetch.MONITOR_STATUS_ALERT:
            block_color = render.COLORS['red']
        elif data == fetch.MONITOR_STATUS_WARN:
            block_color = render.COLORS['orange']
        elif data == fetch.MONITOR_STATUS_NO_DATA:
            block_color = render.COLORS['grey']

        draw_flat_wall(mc=self.mc, pos1=self.pos1, pos2=self.pos2, layout=self.layout, border=False, data=[1.0], filled=WOOL, block_data=block_color)


TYPES = {
    'wall': Wall,
    'mountain': Mountain,
    "status_check": StatusCheck,
    "monitor_status": MonitorStatus,
}
