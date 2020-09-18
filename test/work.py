if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "pygnet"

import matplotlib.pyplot as plt
import random
import numpy as np
from test import persons, Person
from pygnet.algorithms.path import dijkstra, minimum_spanning_tree
from pygnet import Graph, Node, VECTOR

_, ax = plt.subplots(2, 2, squeeze=False)


class VisualTest:
    def test_dijkstra_vis(self):
        with Graph(type='vector') as g:
            for i in range(6):
                g.add_node(Node(i))
            edges = [(0, 1, 2), (0, 2, 10), (1, 3, 10),
                     (1, 4, 8), (2, 5, 2), (3, 2, 7), (4, 5, 5)]
            for e in edges:
                g.add_edge(*e)
            # print(g.graph_matrix)
            print(g.DFS())
            cost = dijkstra(g, 0, 5, path=True)
            # print(cost)
            for i, c in enumerate(cost):
                if i < len(cost)-1:
                    edge = g.connections[g.get_node_id(
                        cost[i])][g.get_node_id(cost[i+1])]
                    edge.color = "red"
                    edge.fontsize = 0.5
                c.color = "green"
                c.radius = -0.5
            g.display(weighted=True, polygon_radius=1, ax=ax[0, 0])
            # plt.show()

    def test_custom_object(self):
        with Graph(ref="name", type=VECTOR) as h:
            obj = []
            for pes in persons:
                obj.append(Person(**pes))
            h.add_nodes_from_iterable(obj)
            h.add_edge("sam", "sarah")
            h.add_edge("sam", "jane")
            h.add_edge("frank", "jane")
            print(h["jane"].adjacent_nodes)
            h["sam"].color = "#ee2341"
            h["frank"].color = "green"
            h.display(layout="polygon", attr="sex")
            # plt.show()

    def test_mst_vis(self):
        with Graph() as mst:
            mst.add_nodes_from_iterable(range(1, 9))
            edge_list = [(1, 2, 4), (1, 5, 2), (1, 4, 10), (2, 4, 8), (2, 3, 18), (3, 4, 11), (
                3, 8, 19), (4, 5, 5), (4, 7, 11), (4, 8, 9), (5, 6, 51), (6, 7, 1), (6, 8, 2), (7, 8, 23)]
            mst.add_edges_from_iterable(edge_list)
            mst[1].color = 'green'
            mst[5].color = '#32a8a4'
            mst[2].color = "#e299ff"
            mst.display(weighted=True, layout="polygon", ax=ax[0, 1])
            print(mst.graph_matrix)
            sub = minimum_spanning_tree(mst)
            sub.display(weighted=True, layout="polygon", ax=ax[1, 0])
            # plt.show()
            print(sub.graph_matrix)

    def test_multiple_random_nodes(self, n, e):
        with Graph() as r:
            nodes = [random.randint(1, 50) for _ in range(n)]
            edges = [(random.choice(nodes), random.choice(nodes),
                      random.randint(0, 50)) for _ in range(e)]
            r.add_nodes_from_iterable(nodes)
            r.add_edges_from_iterable(edges)
            for e in edges:
                r.connections[e[0]][e[1]].color = "red"
            r.display(layout="random", weighted=True, ax=ax[1, 1])
            # plt.show()


if __name__ == "__main__":
    cases = VisualTest()
    # cases.test_mst_vis()
    cases.test_dijkstra_vis()
    # cases.test_multiple_random_nodes(10, 20)
    plt.show()
