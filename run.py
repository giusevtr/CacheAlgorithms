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


def getLowLim(data, i):
    n = data.shape[1] # columns
    m = data.shape[0] # rows
    arr = np.array([])
    
    for j in range(0,n):
        y = data[i, j]
        x = 0
        V = np.append(data[0:i,j],data[i+1:m,j])
        for v in V :
            if v < y and v > x:
                x = v
        arr = np.append(arr, x)
    
    return arr

if __name__ == "__main__" :
    INPUT_CONFIG_FILE = 'config/input_data_location.txt'
    
    if os.path.isfile(INPUT_CONFIG_FILE) :
        f = open(INPUT_CONFIG_FILE, 'r')
        DATA_FOLDER = f.readline().rstrip('\n\r')
    else:
        print('%s not found')
        sys.exit(0)
    
    OUTPUT_FOLDER='output/'
    
    if len(sys.argv) <= 3 :
        print('Must provide more than 3 arguments')
        sys.exit(0)

    cache_size = int(sys.argv[1])
    experiment_name = sys.argv[2]
    algorithm = sys.argv[3:]
    
    ###############################################################
    ## Plot title
    ###############################################################
    subtitle = '\nfile name: %s\n' % experiment_name
    plt.title(subtitle)
    
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
        hits, part_hit_rate, hit_sum = algo.test_algorithm(pages, partition_size=cache_size*4)
        
        ########################
        ## Plot internal state
        ########################
        ax = plt.subplot(2,1,1)
        ax.set_title('%s internal state' % name)
        ax.set_ylim(0,1)
        algo.visualize(plt)
        temp = 1751
#         plt.axvline(x=temp,color='b')
#         plt.axvline(x=10000+temp,color='r')

        data.append(part_hit_rate)
        hit_rate.append(round(100.0 * hits / num_pages,2))
        # print('%s\t%f\t\t%d\t\t%d\t\t%d' % (lower_name, 100.0 * hits / num_pages, hits, num_pages, trace_obj.unique_pages()))
        print("{:<20} {:<20} {:<20} {:<20}  {:<20}".format(name, round(100.0 * hits / num_pages,2), hits, num_pages, trace_obj.unique_pages()))

        sys.stdout.flush()
    data = np.array(data)
    print('=====================================================')

    #####################
    ## Plot performance #
    #####################
    ax = plt.subplot(2,1,2)
    #ax.set_title('file name: %s\n' % experiment_name)
    ax.set_ylim(-.05,1.05)
    rows = data.shape[0]
    cols = data.shape[1]
    T = np.array(range(0,cols))
    plt.axvline(x=cols/2)
    cnt = rows
#     plt.stackplot(T,data,baseline='wiggle')
    for i in range(0,rows):        
        upper = data[i,:]
        lower = getLowLim(data, i)
#         plt.fill_between(T, lower,upper, facecolor=colors[i],alpha=0.3,label=algorithm[i])
#         plt.fill_between(T, 0,data[i,:], facecolor=colors[i],alpha=1,label=algorithm[i])
#         plt.style.use('fivethirtyeight')
#         l, = plt.plot(T,upper,c=colors[i],label=algorithm[i])
        l, = plt.plot(T,upper,c=colors[i],label=algorithm[i],alpha=1,linewidth=(rows-i)*2)
        labels.append(l)
#         patch = mpatches.Patch(color=colors[i], label=algorithm[i])
#         labels.append(patch)
#     l, = plt.plot(T,data[rows-1,:], colors[rows-1]+'-', label=algorithm[rows-1])
#     labels.append(l)

    hit_rate_text = 'algorithm:  hit-rate\n'
    for i in range(0, rows) :
        hit_rate_text += '%s:  %f\n' % (algorithm[i], hit_rate[i])
    ax.annotate(hit_rate_text,(0.05,0.1),textcoords='axes fraction',alpha=0.7, size=12)
    
    plt.xlabel('Request Window Number')
    plt.ylabel('Hit Rate')
    plt.legend(handles=labels,fancybox=True, framealpha=0.5)

    
    outfilename =OUTPUT_FOLDER+experiment_name+'_'+str(cache_size)+'.jpeg' 
    
    print(outfilename)
    plt.savefig(outfilename)
#     plt.show()
