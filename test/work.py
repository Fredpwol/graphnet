if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "pygnet"

from pygnet import Graph, Node, VECTOR
from pygnet.algorithms.search import DFS
from pygnet.algorithms.path import dijkstra, minimum_spanning_tree
from test import persons, Person
import matplotlib.pyplot as plt 

# with Graph(type='vector') as g:
#     for i in range(6):
#         g.add_node(Node(i))
#     edges = [(0,1,2),(0,2,10),(1,3,10),(1,4,8),(2,5,2),(3,2,7),(4,5,5)]
#     for e in edges:
#         g.add_edge(*e)
#     print(g.graph_matrix)
#     print(g.DFS())
#     cost = dijkstra(g,0,5,path=True)
#     print(cost)
#     for i, c in enumerate(cost):
#         if i < len(cost)-1:
#             edge = g.connections[g.get_node_id(cost[i])][g.get_node_id(cost[i+1])]
#             edge.color = "red"
#             edge.fontsize = 20
#         c.color = "green"
#         c.radius = -0.5
#     g.display(weighted=True, polygon_radius=1)
#     plt.show()

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
    h.display(layout="polygon")
    plt.show()

# with Graph() as mst:
#     mst.add_nodes_from_iterable(range(1,9))
#     edge_list = [(1,2,4),(1,5,2),(1,4,10),(2,4,8),(2,3,18),(3,4,11),(3,8,19),(4,5,5),(4,7,11),(4,8,9),(5,6,51),(6,7,1),(6,8,2),(7,8,23)]
#     for e in edge_list:
#         mst.add_edge(*e)
#     mst[1].color = 'green'
#     mst[5].color = '#32a8a4'
#     mst[2].color = "#e299ff"
#     mst.display(weighted=True, layout="polygon")
#     plt.show()
#     print(mst.graph_matrix)
#     sub = minimum_spanning_tree(mst)
#     print(sub.connections)
#     sub.display(weighted=True, layout="polygon")
#     plt.show()
#     print(sub.graph_matrix)