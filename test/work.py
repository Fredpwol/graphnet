from pygnet import Graph, Node
from pygnet.algorithms.search import DFS
from pygnet.algorithms.path import dijkstra



g = Graph(type='vector')
for i in range(6):
    g.add_node(Node(i))
edges = [(0,1,2),(0,2,10),(1,3,10),(1,4,8),(2,5,2),(3,2,7),(4,5,5)]
for e in edges:
    g.add_edge(*e)
print(g.graph_matrix)
cost = dijkstra(g,0,5,path=True)
print(cost)