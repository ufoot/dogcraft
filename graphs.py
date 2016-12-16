import os
from fetch import get_simple_data, get_demo_data
from render import draw_flat_wall, erase_flat_wall


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

    def cleanup(self):
        raise Exception("Not implemented")

    def get_data(self):
        if os.environ.get('DATADOG_DEMO_DATA'):
            return get_demo_data()
        return get_simple_data(self.query)


class Wall(AbstractGraph):

    def update(self):
        data = self.get_data()
        draw_flat_wall(mc=self.mc, pos1=self.pos1, pos2=self.pos2,
                       layout=self.layout, border=self.border, data=data)
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


TYPES = {
    'wall': Wall,
    'mountain': Mountain,
    "status_check": StatusCheck,
}
