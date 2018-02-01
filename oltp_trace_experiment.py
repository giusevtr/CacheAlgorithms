import sys
import os
import numpy as np
from algorithms.OPT import OPT
from algorithms.ARCOPT import ARCOPT
from algorithms.LRU import LRU
from algorithms.LFU import LFU
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
from algorithms.BANDIT2 import BANDIT2
from algorithms.BANDIT3 import BANDIT3


from lib.random_graph import Graph
from lib.traces import Trace

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

if __name__ == "__main__" :
    print('debug')
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


    subplot = 0 
    for file_numer, file_name in enumerate(f):
        if file_numer not in {0} :
            continue
        subplot += 1

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
        
        data = []
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
            elif lower_name == 'lfu' :
                algo = LFU(cache_size)
            elif lower_name == 'lfu1' :
                algo = LFU(cache_size,decay=1)
            elif lower_name == 'lfu2' :
                algo = LFU(cache_size,decay=0.9)
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
            elif lower_name == 'bandit2' :
                algo = BANDIT2(cache_size)
            elif lower_name == 'bandit3' :
                algo = BANDIT3(cache_size)    

            hits, part_hit_rate, hit_sum = algo.test_algorithm(pages, partition_size=200)
            
            
            if lower_name == 'bandit3' or lower_name == 'bandit2':
                plt.subplot(2,2,subplot)
#                 plt.title('s')
                algo.vizualize(plt)
            
            ## Plot algorithm
            X = np.arange(0, len(hit_sum),1)
#             l, = plt.plot(X, hit_sum, colors[color_id]+'-',label=name)
#             labels.append(l)
            
#             plt.subplot(2,2,subplot+2)
            
#             T = np.array(range(0,len(part_hit_rate)))
#             l, = plt.plot(T, part_hit_rate, colors[color_id]+'-',label=name)
#             labels.append(l)
#             color_id += 1
            
            data.append(part_hit_rate)
            
#             print(hit_sum)
            max_column_height = max(max_column_height, hit_sum[-1])

            # print('%s\t%f\t\t%d\t\t%d\t\t%d' % (lower_name, 100.0 * hits / num_pages, hits, num_pages, trace_obj.unique_pages()))
            print("{:<20} {:<20} {:<20} {:<20}  {:<20}".format(lower_name, round(100.0 * hits / num_pages,2), hits, num_pages, trace_obj.unique_pages()))

            sys.stdout.flush()

        print('=====================================================')

        plt.subplot(2,2,subplot+2)
        data = np.array(data).T
        col = data.shape[1]
        T = np.array(range(0,len(data)))
        for i in range(0,col-1):
#             plt.fill(T, data[:,i], colors[i],alpha=0.3)
            plt.fill_between(T, 0,data[:,i], facecolor=colors[i],alpha=0.3,label=algorithm[i])
#             plt.fill_between(T, 0,data[:,i])
        
        
        lru_patch = mpatches.Patch(color=colors[0], label=algorithm[0])
        lfu_patch = mpatches.Patch(color=colors[1], label=algorithm[1])
        
        l, = plt.plot(T,data[:,2], colors[2]+'-', label=algorithm[2])
        labels.append(lru_patch)
        labels.append(lfu_patch)
        labels.append(l)
        plt.xlabel('Request Window Number (200 request)')
        plt.ylabel('Hit Rate')
        
        plt.legend(handles=labels)
        
    plt.show()
