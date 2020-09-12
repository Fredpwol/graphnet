import numpy as np
import matplotlib.pyplot as plt 



def preproccess_plot(func):

    def wrapper(graph, ax, n, weighted, shrinkA, shrinkB, *args, **kwargs):
        space = np.linspace(0,1,n+1)
        wrapper.scale = 100 // (n+1)
        size = wrapper.scale + 10
        x = []
        for i in range(0, len(space)-1):
            point = (space[i]+space[i+1]) / 2
            x.append(point)
        y = [np.random.random() for _ in range(n)]
        for i, node in enumerate(graph):
            wrapper.points[node] = (x[i], y[i])

        func(graph, ax, n, weighted, shrinkA, shrinkB, *args, **kwargs)
        for i, node in enumerate(graph):
            ax.plot(x[i], y[i], "o",markersize=size, color=node.color)

        for node in wrapper.points:
            #
            x, y = wrapper.points[node]
            value = graph.get_node_id(node)
            ax.annotate(value, (x, y))
    wrapper.scale = 0
    wrapper.points = dict()
    return wrapper