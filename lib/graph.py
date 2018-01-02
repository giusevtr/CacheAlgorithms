import numpy as np
class Graph :

    def __init__(self) :
        self.G = {}
        self.edge_set = set()

    ## Increases the weight of edge (u,v)
    def increase_edge_weight(self, u,v, w = 1) :

        if (u,v) not in self.edge_set :
            self.add_edge(u,v,w)
        else :
            self.G[u][v] += w

    ## Create an edge (u,v) with weight 'w'
    def add_edge(self, u,v, w = 1) :
        if u not in self.G :
            self.G[u] = {}
        if v not in self.G :
            self.G[v] = {}

        self.G[u][v] = w
        self.edge_set = self.edge_set | {(u,v)}

    def get_adj_matrix(self, use_weights = True) :
        ## Mapping
        node_id = {}
        node_name = {}
        for i,node in enumerate(self.G) :
            node_id[node] = i
            node_name[i] = node

        A = np.zeros((len(node_id),len(node_id)))
        for u in self.G :
            adj = list(self.G[u])
            for v in adj:
                if v in self.G :
                    u_id = node_id[u]
                    v_id = node_id[v]

                    if use_weights :
                        A[u_id,v_id] = self.G[u][v]
                        A[v_id,u_id] = self.G[u][v]
                    else :
                        A[u_id,v_id] = 1
                        A[v_id,u_id] = 1
                else :
                    self.G[u].pop(v, None)

        # print(A)
        ## Normalize
        for u in range(len(A)) :
            degree = np.sum(A[u,:])
            if degree > 0:
                A[u,:] /= degree

        return A,node_id,node_name

    def get_edge_weight(self, u,v) :
        return self.G[u][v]

    def __contains__(self, e) :

        return e[0] in self.G and e[1] in self.G and e in self.edge_set

    def remove_vertex(self, v) :
        self.G.pop(v, None)
