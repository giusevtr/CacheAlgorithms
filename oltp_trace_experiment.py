import sys
import os
import numpy as np
from algorithms.OPT import OPT
from algorithms.ARCOPT import ARCOPT
from algorithms.LRU import LRU
from algorithms.ARC import ARC
from algorithms.MARKING import MARKING
from algorithms.WALK_MARKING_SLOW import WALK_MARKING_SLOW
from algorithms.WALK_MARKING import WALK_MARKING
from algorithms.PAGERANK_MARKING_SLOW import PAGERANK_MARKING_SLOW
from algorithms.PAGERANK_MARKING_FAST import PAGERANK_MARKING_FAST
from algorithms.FAR import FAR
from algorithms.ExpertLearning import ExpertLearning
from algorithms.ExpertLearning_v2 import ExpertLearning_v2
from algorithms.ExpertLearning_v3 import ExpertLearning_v3
from algorithms.RANDOM import RANDOM
from algorithms.ANN1 import ANN1
from algorithms.BANDIT import BANDIT



from lib.random_graph import Graph
from lib.traces import Trace

import matplotlib.pyplot as plt

if __name__ == "__main__" :

    if len(sys.argv) < 3 :
        print('Must provide 2 arguments')
        print('First argument is the cache size.')
        print('Then come the algotithms to test. Ex:')
        print('python oltp_trace_experiment.py 100 lru arc far')
        sys.exit(0)

    cache_size = int(sys.argv[1])
    algorithm = sys.argv[2:]

    ###############################################################
    ## Read data
    ###############################################################
    trace_obj = Trace()
    f = open('config.txt', 'r')


    for file_numer, file_name in enumerate(f):
        if file_numer not in {0} :
            continue

        file_name = file_name[:-1]
        # print('Reading file: ', file_name)
        print ('file = %s' % file_name)
        print ('cache size = %s' % (cache_size))
        trace_obj.read(file_name)

        pages = trace_obj.get_request()
        num_pages = len(pages)

        # print('name\t\thit ratio\t\thit count\ttotal request\tunique pages')
        print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("Name","Hit Ratio(%)", "Hit Count", "Total Request","Unique Pages" , "Partition Hit-Rates") )

        colors = ['y','b','r','k','g']
        color_id = 0
        labels = []
        max_column_height = 0
        
        for name in algorithm :
            lower_name = name.lower()
            if lower_name == 'arc' :
                algo = ARC(cache_size)
            elif lower_name == 'arcopt' :
                algo = ARCOPT(cache_size, pages)
            elif lower_name == 'marking' :
                algo = MARKING(cache_size)
            elif lower_name == 'opt' :
                algo = OPT(cache_size, pages)
            elif lower_name == 'lru' :
                algo = LRU(cache_size)
            elif lower_name == 'pagerank_fast' :
                algo = PAGERANK_MARKING_FAST(cache_size)
            elif lower_name == 'pagerank_slow' :
                algo = PAGERANK_MARKING_SLOW(cache_size)
            elif lower_name == 'walk' :
                algo = WALK_MARKING(cache_size)
            elif lower_name == 'walkslow' :
                algo = WALK_MARKING_SLOW(cache_size)
            elif lower_name == 'far' :
                algo = FAR(cache_size)
            elif lower_name == 'expertlearning' :
                algo = ExpertLearning(cache_size)
            elif lower_name == 'expertlearning_v2' :
                algo = ExpertLearning_v2(cache_size)
            elif lower_name == 'expertlearning_v3' :
                algo = ExpertLearning_v3(cache_size)
            elif lower_name == 'random' :
                algo = RANDOM(cache_size)
            elif lower_name == 'ann1' :
                M  = trace_obj.unique_pages()
                print('M = ', M)
                algo = ANN1(M, cache_size)
            elif lower_name == 'bandit' :
                algo = BANDIT(cache_size)
                

            hits, part_hit_rate, hit_sum = algo.test_algorithm(pages)

            ## Plot algorithm
            X = np.arange(0, len(hit_sum),1)
            l, = plt.plot(X, hit_sum, colors[color_id]+'-',label=name)
            labels.append(l)
            color_id += 1

            max_column_height = max(max_column_height, hit_sum[-1])

            # print('%s\t%f\t\t%d\t\t%d\t\t%d' % (lower_name, 100.0 * hits / num_pages, hits, num_pages, trace_obj.unique_pages()))
            print("{:<20} {:<20} {:<20} {:<20}  {:<20}".format(lower_name, round(100.0 * hits / num_pages,2), hits, num_pages, trace_obj.unique_pages()) , part_hit_rate)

            sys.stdout.flush()

        print('=====================================================')


        ####################################################################################3
        ## Count unique pages
        ## Unique pages
        N = len(pages)

        unique_page_set = set()
        number_of_blocks = 100
        unique_page_block_size = N / number_of_blocks

        X = np.array([-unique_page_block_size/2])
        Y = np.array([0])

        for ith_page, page in enumerate(pages) :
            unique_page_set.add(page)

            if ith_page % unique_page_block_size == 0 :
                col_position = X[-1] + unique_page_block_size
                col_height = len(unique_page_set)
                # print col_position,col_height

                X = np.append(X, col_position)
                Y = np.append(Y, col_height)

                unique_page_set.clear()

        Y2 = ((1.0 * Y / max(Y)) * max_column_height)
        plt.bar(X,Y2,alpha=0.4, width = unique_page_block_size, color='r')
        #print X,Y2
        ####################################################################################3


        plt.legend(handles=labels)
        #plt.show()
