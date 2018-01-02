import sys
import numpy as np
from algorithms.LRU import LRU
from algorithms.ARC import ARC
from algorithms.MARKING import MARKING
from algorithms.PAGERANK_MARKING import PAGERANK_MARKING
from lib.random_graph import Graph
from lib.traces import Trace

import matplotlib.pyplot as plt

if __name__ == "__main__" :

    algorithm = sys.argv[1]
    cache_size = int(sys.argv[2])
    number_of_nodes = int(sys.argv[3])
    number_of_edges = int(sys.argv[4])


    number_of_experiments = 500
    faults_sum = 0
    results = np.array([])
    for _0 in range(number_of_experiments) :

        g = Graph()
        g.create_random_undirected_graph(number_of_nodes,number_of_edges)

        if algorithm.lower() == 'arc' :
            algo = ARC(cache_size)
        elif algorithm.lower() == 'marking' :
            algo = MARKING(cache_size)
        elif algorithm.lower() == 'lru' :
            algo = LRU(cache_size)
        elif algorithm.lower() == 'pagerank' :
            algo = PAGERANK_MARKING(cache_size)
            # algo.set_random_graph(g)


        # g.debug_graph()

        x = 0
        page_faults = 0
        for _1 in range(1000) :

            if not algo.request(x) :
                page_faults += 1

            x = g.get_rand_adj_node(x)
        faults_sum += page_faults
        results = np.append(results, page_faults)
        # print('page faults: ', page_faults)

    print('avg = %f\tstd = %f' % (np.average(results), np.std(results)))
    # plt.plot(results)
    n, bins, patches = plt.hist(results, 25, normed=1, facecolor='green', alpha=0.75)
    plt.show()
