from ..exceptions import GraphTypeError
from ..utils import GraphPriorityQueue


def dijkstra(graph, _from, _to, path=False):
    if graph.is_cyclic():
        raise GraphTypeError("Graph contains circle.")
    elif graph.type != 'vector':
        raise GraphTypeError("Graph type most be vector not %s"%(graph.type))
    
    ref = graph.ref
    source = graph[_from]
    dist = {}
    for node in graph:
        dist[node] = float('inf')
    if path:
        route = {}
        route[source] = [source]
    Q = GraphPriorityQueue(graph, type='min', state=True)
    Q.enqueue(source)
    dist[source] = 0
    while not Q.is_empty():
        node = Q.get()
        node_id = node_id = eval("node.%s"%(ref))
        for neighbour in node.adjacent_nodes:
            neigh_id = eval("neighbour.%s"%(ref))
            if dist[neighbour] > dist[node] + graph.connections[node_id][neigh_id].weight:
                dist[neighbour] = dist[node] + graph.connections[node_id][neigh_id].weight
                if path:
                    route[neighbour] = route[node] + [neighbour]
        Q.set_state(node, True)
    to = graph[_to]
    res = dist[to] if not path else route[to]

    return res

    