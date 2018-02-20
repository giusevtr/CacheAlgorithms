import sys
import os
import numpy as np
from algorithms.GetAlgorithm import GetAlgorithm
from lib.traces import Trace
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

##
## python cache_size experiment_name algorithms
##


if __name__ == "__main__" :
    INPUT_CONFIG_FILE = 'config/input_data_location.txt'
    
    if os.path.isfile(INPUT_CONFIG_FILE) :
        f = open(INPUT_CONFIG_FILE, 'r')
        DATA_FOLDER = f.readline()
    else:
        print('%s not found')
        sys.exit(0)
    
    OUTPUT_FOLDER='output/'
    
    print('len(sys.argv) = ', len(sys.argv), sys.argv)
    if len(sys.argv) <= 3 :
        print('Must provide more than 3 arguments')
        sys.exit(0)

    cache_size = int(sys.argv[1])
    experiment_name = sys.argv[2]
    algorithm = sys.argv[3:]
    
    ###############################################################
    ## Read data
    ###############################################################
    trace_obj = Trace()
    trace_obj.read(DATA_FOLDER+experiment_name)
    pages = trace_obj.get_request()
    num_pages = len(pages)

    colors = ['y','b','r','k','g']
    color_id = 0
    labels = []
    max_column_height = 0
    
    data = []
    hit_rate = []
    print("{:<20} {:<20} {:<20} {:<20} {:<20}".format("Name","Hit Ratio(%)", "Hit Count", "Total Request","Unique Pages" ) )
    for name in algorithm :
        algo = GetAlgorithm(cache_size, name)
        hits, part_hit_rate, hit_sum = algo.test_algorithm(pages, partition_size=200)
        
        ########################
        ## Plot internal state
        ########################
        ax = plt.subplot(2,1,1)
        ax.set_title('%s internal state' % name)
        algo.visualize(plt)
        temp = 1751
#         plt.axvline(x=temp,color='b')
#         plt.axvline(x=10000+temp,color='r')

        data.append(part_hit_rate)
        hit_rate.append(round(100.0 * hits / num_pages,2))
        # print('%s\t%f\t\t%d\t\t%d\t\t%d' % (lower_name, 100.0 * hits / num_pages, hits, num_pages, trace_obj.unique_pages()))
        print("{:<20} {:<20} {:<20} {:<20}  {:<20}".format(name, round(100.0 * hits / num_pages,2), hits, num_pages, trace_obj.unique_pages()))

        sys.stdout.flush()
    data = np.array(data).T
    print('=====================================================')

    #####################
    ## Plot performance #
    #####################
    ax = plt.subplot(2,1,2)
    ax.set_title('file name: %s\n' % experiment_name)
    
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

    subtitle = ''
    for i,al in enumerate(algorithm) :
        subtitle += al
        if i < len(algorithm)-1:
            subtitle += ' vs '
    plt.suptitle(subtitle)
    
    outfilename =OUTPUT_FOLDER+experiment_name+'_'+str(cache_size)+'.jpeg' 
    
    print(outfilename)
    plt.savefig(outfilename)
#     plt.show()
