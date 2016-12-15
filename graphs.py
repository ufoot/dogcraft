
class AbstractGraph(object):

    def __init__(self, graph_conf, mc):
        self.pos1 = graph_conf['pos1']
        self.pos2 = graph_conf['pos2']
        self.query = graph_conf['query']
        self.mc = mc

    def update(self):
        raise Exception("Not implemented")

class Wall(AbstractGraph):

    def update(self):
        self.mc.postToChat("Updating wall")
        pass

class Mountain(AbstractGraph):

    def update(self):
        self.mc.postToChat("Updating montain")
        pass

class StatusCheck(AbstractGraph):

    def update(self):
        # TODO Call the display function
        pass


TYPES = {
    'wall': Wall,
    'mountain': Mountain,
    "status_check": StatusCheck,
}
