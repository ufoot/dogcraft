import yaml
from graphs import TYPES


class Dashboard(object):

    def __init__(self, config_file, mc):
        self.graphs = []
        f = open(config_file, 'r')
        conf = yaml.load(f)
        for graph_conf in conf:
            graph_type = graph_conf['type']
            graph = TYPES[graph_type](graph_conf, mc)
            self.graphs.append(graph)

    def update(self):
        for graph in self.graphs:
            graph.update()

if __name__ == '__main__':
    d = Dashboard("config/dashboard.yaml")
