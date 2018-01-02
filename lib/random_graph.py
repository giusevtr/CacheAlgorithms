import random
import sys


class Graph :

    def __init__(self) :
        self.K = 20
        self.adj = {}
        self.edges = set()

    def clear_graph(self) :
        self.adj.clear()
        self.edges.clear()

    def get_edges(self):
        return self.edges

    def add_edge(self,u,v) :
        if u not in self.adj :
            self.adj[u] = []
        if v not in self.adj :
            self.adj[v] = []
        self.adj[u].append(v)
        self.edges.add((u,v))

    def get_rand_adj_node(self, u) :
        l = len(self.adj[u])
        if l == 0 :
            return None
        i = random.randint(0, l - 1)
        return self.adj[u][i]

    def create_random_undirected_graph(self,num_vertices,num_edges) :
        self.N = num_vertices
        self.E = num_edges

        ## Make sure that the number of edges is not too large
        self.E = min(self.E, self.N * (self.N-1) )

        N = self.N
        E = self.E
        ## Create a random graph with N nodes and E edges
        self.clear_graph()

        ## Set of all possible edges
        remaining_edges = set()
        for u in range(0, N) :
            for v in range(u+1, N) :
                remaining_edges = remaining_edges | {(u,v)}
                remaining_edges = remaining_edges | {(v,u)}

        for u in range(self.N) :
            v = u
            while u == v:
                v = random.randint(0, self.N - 1)
            self.add_edge(u,v)
            remaining_edges = remaining_edges | {(u,v)}
            E-=1

        for _ in range(E) :
            ## Choose a random edge
            k = random.randint(0, len(remaining_edges) - 1)

            e = list(remaining_edges)[k]
            self.add_edge(e[0],e[1])
            # self.add_edge(e[1],e[0])
            remaining_edges = remaining_edges - {e}

    def create_k_regular_graph(self, N, k) :
        self.N = N
        self.E = N * 2
        ## Idea here is to construct a euler graph.
        ## The conditions for existence is that N * k is even which means that the sum of the degrees will be even
        ## Therefore we can construct an euler graph by randomly walking in the graph. The only constrain is that
        ## we walk towards an edge that have k-1 degree unless we don't have anyother choice.

    def size(self) :
        return self.N

    def debug_graph(self) :
        for u in self.adj :
            print(u,":\t" , self.adj[u])


if __name__ == "__main__" :
    ## Usage
    ## python3 random_graph.py <number of random request> <graph type> <params>

    request_size = int(sys.argv[1])
    graph_type = str(sys.argv[2])

    g = Graph()

    if graph_type == 'regular' :
        nodes = int(sys.argv[3])
        k = int(sys.argv[4])
        g.create_k_regular_graph(node,k)
    if graph_type == 'random_undir' :
        nodes = int(sys.argv[3])
        edges = int(sys.argv[4])
        g.create_random_undirected_graph(nodes,edges)

    current_node = 0 # Start at node 0
    for _ in range(request_size) :
        print(current_node)
        current_node = g.get_rand_adj_node(current_node)
