if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

from pygnet import Graph, Node
from pygnet.algorithms.search import DFS
from pygnet.algorithms.path import dijkstra, minimum_spanning_tree
import matplotlib.pyplot as plt 

with Graph(type='vector') as g:
    for i in range(6):
        g.add_node(Node(i))
    edges = [(0,1,2),(0,2,10),(1,3,10),(1,4,8),(2,5,2),(3,2,7),(4,5,5)]
    for e in edges:
        g.add_edge(*e)
    print(g.graph_matrix)
    cost = dijkstra(g,0,5,path=True)
    print(cost)
    for c in cost:
        c.color = "red"
    g.display(weighted=True)
    plt.show()

# with Graph() as mst:
#     mst.add_nodes_from_iterable(range(1,9))
#     edge_list = [(1,2,4),(1,5,2),(1,4,10),(2,4,8),(2,3,18),(3,4,11),(3,8,19),(4,5,5),(4,7,11),(4,8,9),(5,6,51),(6,7,1),(6,8,2),(7,8,23)]
#     for e in edge_list:
#         mst.add_edge(*e)
#     mst[1].color = 'green'
#     mst[5].color = '#32a8a4'
#     mst[2].color = "#e299ff"
#     mst.display(weighted=True)
#     plt.show()
#     print(mst.graph_matrix)
#     sub = minimum_spanning_tree(mst)
#     print(sub.connections)
#     sub.display(weighted=True)
#     plt.show()
#     print(sub.graph_matrix)