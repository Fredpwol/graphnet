from graph import Graph
from components import Node
import random


class GraphPriorityQueue:

    def __init__(self, graph, type="min", state=False):
        self.type = type
        self.graph = graph
        self.__top = float('inf')        
        self.queue = dict()
        self.__state = state
        for node in self.graph:
            self.queue[node] = float('inf')
        if self.__state:
            self.status = dict()
            for node in self.graph:
                self.status[node] = False
        

    def __repr__(self):
        return str(list(self.queue.values))



    def get(self):
        if len(self.queue != 0):
            res = 0
            sign = "<=" if self.type == "min" else ">=" if self.type == "max" else ''
            if not self.__state:
                for node in self.graph:
                    if eval(f"self.queue[{node}] {sign} self.__top"):
                        self.__top = self.queue[node]
                        res = node
            else:
                for node in self.graph:
                    if eval(f"self.queue[{node}] {sign} self.__top) and (not self.status[{node}]"):
                        self.__top = self.queue[node]
                        res = node
            del self.queue[res]
            del self.status[res]
            return res
        else:
            return None
        
    def update_state(self, node, value):
        self.status[node] = value
    

    def update_queue(self, node , value):
        self.queue[node] = value



if __name__ == "__main__":
    g = Graph()
    for i in range(10):
        n = Node(i)
        g.add_node(n)

    q = GraphPriorityQueue(g)
    for node in g:
        val = random.randint(1,11)
        q.update_queue(node,val)

    print(q)
    for _ in range(10):
        print(q.get())
    