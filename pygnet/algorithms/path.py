from ..exceptions import GraphTypeError
from pygnet import GraphPriorityQueue
from ..graph import Graph


def dijkstra(graph, _from, _to, path=False):
    if graph.is_cyclic():
        raise GraphTypeError("Graph contains circle.")
    elif graph.type != 'vector' or  graph.type == 'V':
        raise GraphTypeError("Graph type most be vector not %s"%(graph.type))

    source = graph[_from]
    dist = {}
    for node in graph:
        dist[node] = float('inf')
    if path:
        route = {}
        route[source] = [source]
    Q = GraphPriorityQueue(graph, type='min', state=True)
    Q.enqueue(source,0)
    dist[source] = 0
    while not Q.is_empty():
        print(Q)
        node = Q.get()
        node_id = graph.get_node_id(node)
        for neighbour in node.adjacent_nodes:
            neigh_id = graph.get_node_id(neighbour)
            if dist[neighbour] > dist[node] + graph.connections[node_id][neigh_id].weight:
                dist[neighbour] = dist[node] + graph.connections[node_id][neigh_id].weight
                if path:
                    route[neighbour] = route[node] + [neighbour]
                Q.enqueue(neighbour, dist[neighbour])
        Q.set_status(node, True)
    to = graph[_to]
    res = dist[to] if not path else route[to]

    return res

#TODO Implement bellman ford algorithm,


#TODO Implement minimum spanning tree
def minimum_spanning_tree(graph):
    if graph.type == "scalar" or graph.type == 'S':
        key = {}
        parent = {}
        visited = []
        tree = Graph()
        for node in graph:
            key[node] = float('inf')
            parent[node] = None

        source = graph.get_nodes[0]
        key[source] = 0
        visited.append(source)
        for _ in range(len(graph)-1):
            min_cost = float('inf')
            dest = None
            src = None
            for node in visited:
                for neigh in node.adjacent_nodes:
                    cost = graph.connections[graph.get_node_id(node)][graph.get_node_id(neigh)].weight
                    if cost < min_cost and neigh not in visited:
                        min_cost = cost
                        dest = neigh
                        src = node
            parent[dest] = src
            visited.append(dest)
            key[dest] = min_cost

        for node in parent:
            node.adjacent_nodes.clear()
            tree.add_node(node)            
        
        for node in parent:
            if parent[node] != None:
                tree.add_edge(parent[node], node, key[node])
        return tree
        
    else:
        raise GraphTypeError("Graph type most be vector not %s"%(graph.type))




