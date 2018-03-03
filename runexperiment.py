import sys
import os
import numpy as np
from algorithms.LRU import LRU
from algorithms.LFU import LFU
from algorithms.LFU_DECAY import LFU_DECAY
from algorithms.ARC import ARC
from algorithms.MARKING import MARKING
from algorithms.WALK_MARKING_SLOW import WALK_MARKING_SLOW
from algorithms.WALK_MARKING import WALK_MARKING
from algorithms.PAGERANK_MARKING_SLOW import PAGERANK_MARKING_SLOW
from algorithms.PAGERANK_MARKING_FAST import PAGERANK_MARKING_FAST
from algorithms.FAR import FAR
from algorithms.RANDOM import RANDOM
from algorithms.BANDIT import BANDIT
from algorithms.BANDIT2 import BANDIT2
from algorithms.BANDIT3 import BANDIT3
from algorithms import BANDIT_DOUBLE_HIST
from algorithms.LaCReME import BANDIT_DOUBLE_HIST2
from algorithms.BANDIT_WITH_ARC import BANDIT_WITH_ARC

from lib.traces import Trace
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



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

    DB = {7,8}
    num_db = len(DB)
    subplot = 0
    for file_numer, file_name in enumerate(f):
        if file_numer not in DB :
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
        print("{:<20} {:<20} {:<20} {:<20} {:<20}".format("Name","Hit Ratio(%)", "Hit Count", "Total Request","Unique Pages" ) )

        colors = ['y','b','r','k','g']
        color_id = 0
        labels = []
        max_column_height = 0

        data = []
        hit_rate = []
        for name in algorithm :
            lower_name = name.lower()
            if lower_name == 'arc' :
                algo = ARC(cache_size)
            elif lower_name == 'marking' :
                algo = MARKING(cache_size)
            elif lower_name == 'lru' :
                algo = LRU(cache_size)
            elif lower_name == 'lfu' :
                algo = LFU(cache_size)
            elif lower_name == 'lfu_dacay' :
                algo = LFU_DECAY(cache_size)
            elif lower_name == 'lfu1' :
                algo = LFU_DECAY(cache_size,decay=1)
            elif lower_name == 'lfu2' :
                algo = LFU_DECAY(cache_size,decay=0.9)
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
            elif lower_name == 'random' :
                algo = RANDOM(cache_size)
            elif lower_name == 'bandit' :
                algo = BANDIT(cache_size)
            elif lower_name == 'bandit2' :
                algo = BANDIT2(cache_size)
            elif lower_name == 'bandit3' :
                algo = BANDIT3(cache_size)
            elif lower_name == 'bandit_double_hist' :
                algo = LaCrema(cache_size)   
            elif lower_name == 'bandit_double_hist' :
                algo = LaCrema(cache_size)
            elif lower_name == 'bandit_double_hist2' :
                algo = BANDIT_DOUBLE_HIST2(cache_size)
            elif lower_name == 'bandit_with_arc' :
                algo = BANDIT_WITH_ARC(cache_size)   

            hits, part_hit_rate, hit_sum = algo.test_algorithm(pages, partition_size=200)
            
            if lower_name.startswith('bandit'):
                ax = plt.subplot(2,num_db,subplot)
                ax.set_title('%s internal state' % lower_name)
                algo.visualize(plt)
                temp = 1751
                plt.axvline(x=temp,color='b')
                plt.axvline(x=10000+temp,color='r')
                

            data.append(part_hit_rate)
            hit_rate.append(round(100.0 * hits / num_pages,2))
            # print('%s\t%f\t\t%d\t\t%d\t\t%d' % (lower_name, 100.0 * hits / num_pages, hits, num_pages, trace_obj.unique_pages()))
            print("{:<20} {:<20} {:<20} {:<20}  {:<20}".format(lower_name, round(100.0 * hits / num_pages,2), hits, num_pages, trace_obj.unique_pages()))

            sys.stdout.flush()
        data = np.array(data).T

        print('=====================================================')

        ax = plt.subplot(2,num_db,subplot+num_db)
        ax.set_title('file name: %s\n' % file_name)
        
        col = data.shape[1]
        T = np.array(range(0,len(data)))
        plt.axvline(x=data.shape[0]/2)
        for i in range(0,col-1):
            plt.fill_between(T, 0,data[:,i], facecolor=colors[i],alpha=0.3,label=algorithm[i])
            patch = mpatches.Patch(color=colors[i], label=algorithm[i])
            labels.append(patch)
        l, = plt.plot(T,data[:,col-1], colors[col-1]+'-', label=algorithm[col-1])
        labels.append(l)

        hit_rate_text = 'algorithm:  hit-rate\n'
        for i in range(0, col) :
            hit_rate_text += '%s:  %f\n' % (algorithm[i], hit_rate[i])
        ax.annotate(hit_rate_text,(0.05,0.1),textcoords='axes fraction',alpha=0.7, size=12)
                
        plt.xlabel('Request Window Number')
        plt.ylabel('Hit Rate')

        plt.legend(handles=labels)
    
    ## 
    subtitle = ''
    for i,al in enumerate(algorithm) :
        subtitle += al
        if i < len(algorithm)-1:
            subtitle += ' vs '
    plt.suptitle(subtitle)
    
    plt.show()
