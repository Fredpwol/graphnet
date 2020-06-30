from graph import Graph
from components import Node
import random


class GraphPriorityQueue:

    def __init__(self, graph, type="min", state=False):
        if type == 'min' or type == 'max':
            self.type = type
        else:
            raise TypeError("type attribute most be 'min' or 'max'")
        self.graph = graph
        self._top = float('inf') if self.type == 'min' else -float('inf')       
        self.queue = dict()
        self.__state = state
        for node in self.graph:
            self.queue[node] = float('inf')
        if self.__state:
            self.status = dict()
            for node in self.graph:
                self.status[node] = False
        

    def __repr__(self):
        return str(list(self.queue.values()))



    def get(self):
        if self.__state:
            if all(self.status.values()):
                return None
        if len(self.queue) != 0:
            sign = "<=" if self.type == "min" else ">=" if self.type == "max" else ''
            state = '' if not self.__state else 'and (not self.status[node])'
            for node in self.queue:
                if eval(f"(self.queue[node] {sign} self._top {state})"):
                    self._top = self.queue[node]
                    res = node
            del self.queue[res]
            if self.__state:
                del self.status[res]
            self._top = float('inf') if self.type == 'min' else -float('inf')
            return res
        return None
        
    def set_state(self, node, value):
        assert (value == True or value == False) and (self.__state)
        self.status[node] = value
    

    def enqueue(self, node , value):
        self.queue[node] = value



if __name__ == "__main__":
    g = Graph()
    for i in range(1,11):
        n = Node(i)
        g.add_node(n)

    q = GraphPriorityQueue(g, type='min')
    for node in g:
        val = random.randint(1,10)
        q.enqueue(node,val)

    print(q)
    for _ in range(10):
        print(q.get())
    