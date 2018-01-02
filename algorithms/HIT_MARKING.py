import random
import sys
import numpy as np
from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.random_graph import Graph
from lib.markov_matrix import Markov
from lib.aux import *
from lib.graph import Graph

class HIT_MARKING(page_replacement_algorithm):

    def __init__(self, N):
        self.T = Disk(N)
        self.H = Disk(N)

        self.N = N
        self.marked = set()
        self.G = Graph() ## local access graph

        self.is_first_request = True
        self.last_request = -1

        self.hitting_time = {}

        self.fast_mode = True
        self.use_weights = False
        self.weights = {}

    def request(self,page) :
        # print('request: ', page)
        page_fault = False

        if not self.is_first_request :
            self.G.increase_edge_weight(self.last_request, page,1)

        self.last_request = page
        self.is_first_request = False

        if page in self.T  :
            ## Mark page
            self.marked.add(page)
        else :

            # Start a new phase when all pages are marked and a page fault occurs
            # Unmark all the pages
            if len(self.marked) == self.N :
                self.marked.clear()

                if self.fast_mode is True:
                    self.hitting_time = self.__calculate_hit_time(page)

            if self.T.size() == self.N :

                if self.fast_mode is False :
                    self.hitting_time = self.__calculate_hit_time(page)


                ## Get the set of unmarked pages
                U = set(self.T.get_data()) - self.marked
                U_list = list(U)
                U_dist = []
                for u in U_list :
                    U_dist.append(self.page_probability[u])

                page_to_evict = random_select_page(U_list, U_dist)

                ## Delete page from cache
                self.T.delete(page_to_evict)

                ## Remove least resent page from history
                if self.H.size() == self.N :
                    hist_lru = self.H.deleteFront()
                    if hist_lru is not None and hist_lru in self.G :
                        self.G.pop(hist_lru, None)

            ## Mark page and add to T
            self.marked.add(page)
            self.T.add(page)

            ## Page fault is True
            page_fault = True

        return page_fault

    def __calculate_hit_time(self, init_page) :
        A,node_id,node_name = self.G.get_adj_matrix()

        #######################
        ## Hitting time
        #######################
        # print('R = ',R)

        m = self.G.number_vertices()
        m = self.G.number_edges()



        P = {}
        for u,p in enumerate(R) :
            # print('PR[%s] = %f' % (node_name[u], pr))
            P[node_name[u]] = p

        return P

    ######################################################################################################################################

    def page_label(self,page):
        lab = "%s(%.1f)" % (page, self.page_probability[page] if page in self.page_probability else 0)
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
        return [self.T.get_data()]
