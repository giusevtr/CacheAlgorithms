import random
import sys
import numpy as np
if sys.version_info[0] < 3 :
    import Queue as Q
else :
    import queue as Q

from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.random_graph import Graph
from scipy.sparse import csc_matrix

class FAR(page_replacement_algorithm):

    def __init__(self, N):
        self.T = Disk(N)
        self.N = N
        self.marked = set()
        self.G = {} ## local access graph
        self.last_request = -1
        self.first_request = False
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

            # Start a new phase when all pages are marked and a page fault occurs
            # Unmark all the pages
            if len(self.marked) == self.N :
                self.marked.clear()

            if self.T.size() == self.N :
                ## Get the set of unmarked pages
                U = set(self.T.get_data()) - self.marked

                # Compute the page distance
                # self.PR = self.compute_pagerank(page)
                dist = self.__distance_bfs(page)

                furthest_page = -1
                first = True
                for u in U :
                    # print("u = ",u)
                    if first or dist[u] > dist[furthest_page] :
                        furthest_page = u
                        first = False

                ## Delete page from cache
                self.T.delete(furthest_page)

                ## Remove furthest page from history
                if furthest_page in self.G :
                    # print('G.pop (',u,')')
                    self.G.pop(furthest_page, None)


            ## Mark page and add to T
            self.marked.add(page)
            self.T.add(page)

            ## Page fault is True
            page_fault = True

        return page_fault


    def __distance_bfs(self, u) :
        q = Q.Queue()
        dist = {}
        q.put(u)
        dist[u] = 0
        while not q.empty() :
            u = q.get()
            # print("u = ", u)
            adj = self.G[u]
            for v in adj :
                if v not in dist and v in self.G:
                    if v in self.G :
                        dist[v] = dist[u] + 1
                        q.put(v)
                    else :
                        self.G[u] = self.G[u] - {v}
                    # print("\tv = ", v)
        return dist



    def __add_edge(self, u,v) :
        if u not in self.G :
            self.G[u] = set()
        if v not in self.G :
            self.G[v] = set()

        self.G[u] = self.G[u] | {v}
        self.G[v] = self.G[v] | {u}

    def page_label(self,page):
        lab = "%s" % (page)
        return lab

    def page_color(self,page) :
        if page in self.marked :
            return 1 ## Red
        else :
            return 0 # white


    def get_data(self):
        # data = []
        # for i,p,m in enumerate(self.T):
        #     data.append((p,m,i,0))
        # return data
        return [self.T.get_data()]
