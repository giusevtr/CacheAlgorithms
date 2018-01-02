import random
import sys
import numpy as np
from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.random_graph import Graph
from scipy.sparse import csc_matrix
from lib.pagerank import Pagerank

class PAGERANK_MARKING_FAST(page_replacement_algorithm):

    def __init__(self, N):
        self.T = Disk(N)
        self.H = Disk(N)
        self.N = N
        self.marked = set()
        self.G = {} ## local access graph
        self.last_request = -1
        self.first_request = False
        self.PR = {}
    def get_N(self) :
        return self.N

    def request(self,page) :
        # print('request: ', page)
        page_fault = False

        if not self.first_request :
            self.__add_edge(self.last_request, page)

        self.last_request = page
        self.first_request = False

        if page in self.T  :
            ## Mark page
            self.marked.add(page)
        else :
            if page in self.H :
                self.H.delete(page)

            # Start a new phase when all pages are marked and a page fault occurs
            # Unmark all the pages
            if len(self.marked) == self.N :
                self.marked.clear()
                self.PR = self.compute_pagerank(page)

            if self.T.size() == self.N :
                ## Get the set of unmarked pages
                U = set(self.T.get_data()) - self.marked

                # Compute the page rank of all pages
                # self.PR = self.compute_pagerank(page)

                ## Choose a page with minimum pagerank
                least_pagerank_page = -1
                for u in U :
                    if least_pagerank_page == -1 or self.PR[u] < self.PR[least_pagerank_page] :
                        least_pagerank_page = u

                ## Delete page from cache
                self.T.delete(least_pagerank_page)

                ## Remove least resent page from history
                if self.H.size() == self.N :
                    u = self.H.deleteFront()
                    if u is not None and page in self.G :
                        # print('G.pop (',u,')')
                        self.G.pop(u, None)

                ## Move discarted page to history
                self.H.add(least_pagerank_page)

            ## Mark page and add to T
            self.marked.add(page)
            self.T.add(page)

            ## Page fault is True
            page_fault = True

        return page_fault

    def __add_edge(self, u,v) :
        if u not in self.G :
            self.G[u] = set()
        if v not in self.G :
            self.G[v] = set()

        self.G[u] = self.G[u] | {v}
        self.G[v] = self.G[v] | {u}

    def __get_adj_matrix(self) :
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
                    A[u_id,v_id] = 1
                    A[v_id,u_id] = 1
                else :
                    self.G[u] = self.G[u] - {v}

        return A,node_id,node_name

    def __mult_matrix(self,A,n) :
        B = np.eye(len(A))
        while n > 0 :
            if n % 2 == 1 :
                B = np.matmul(B,A)
            A = np.matmul(A,A)
            n = n / 2
        return B

    def compute_pagerank(self, init_page) :
        A, node_id, node_name = self.__get_adj_matrix()
        u = node_id[init_page]
        n = len(A)

        ## Transportation vector
        E = np.zeros(n)
        E[u] = 1

        # ranks_per_page = pr.compute(A,teleport_vector=tv)
        pr = Pagerank()
        R = pr.compute_local(A,E)

        PR = {}
        for v,pr in enumerate(R) :
            PR[node_name[v]] = pr
        return PR

    def page_label(self,page):
        lab = "%s(%.1f)" % (page, self.PR[page] if page in self.PR else 0)
        return lab

    def page_color(self,page) :
        if page in self.marked :
            return 1 ## Red
        else :
            return 0 # white

    def debug(self) :
        X = []
        for u in self.get_data() :
            X.append((self.P[u],u))

    def get_data(self):
        # data = []
        # for i,p,m in enumerate(self.T):
        #     data.append((p,m,i,0))
        # return data
        return [self.T.get_data(), self.H.get_data()]
