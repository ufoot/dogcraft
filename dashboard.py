import yaml
from graphs import TYPES
from cache import RenderCache


class Dashboard(object):

    def __init__(self, config_file, mc):
        self.graphs = []
        f = open(config_file, 'r')
        conf = yaml.load(f)
        for graph_conf in conf:
            graph_type = graph_conf['type']
            # Now, below, we use a RenderCache instead of a genuine
            # Minecraft object. setBlock should work the same but the
            # other functions... are not there ! Current implem does
            # not use them anyway.
            graph = TYPES[graph_type](graph_conf, RenderCache(mc))
            self.graphs.append(graph)

    def update(self):
        for graph in self.graphs:
            graph.update()

    def cleanup(self):
        for graph in self.graphs:
            graph.cleanup()

if __name__ == '__main__':
    d = Dashboard("config/dashboard.yaml")
