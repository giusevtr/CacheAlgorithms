import sys
import os
import time
import numpy as np
from algorithms.GetAlgorithm import GetAlgorithm
from lib.traces import Trace
import matplotlib.pyplot as plt

##
## python cache_size experiment_name algorithms
##

WINDOW_SIZE = 10
ANNOTATION_HEIGHT = 0.4
#VERTICAL_LINES = {40917 - 20000, 917}
# VERTICAL_LINES = {41754 - 10000, 41754 - 20000,41754 - 30000,41754 - 40000}
VERTICAL_LINES = {}

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
    
    if len(sys.argv) <= 4 :
        print('Must provide more than 3 arguments')
        sys.exit(0)


    assert float(sys.argv[1]) > 0,  'cache_size must be positive'
    
    
    
    cache_size_per = float(sys.argv[1])
    experiment_name = sys.argv[2]
    blocksize = int(sys.argv[3])
    algorithm = sys.argv[4:]
    
    
    ###############################################################
    ## Plot title
    ###############################################################
    subtitle = '\nfile name: %s\n' % experiment_name
    plt.title(subtitle)
    
    ###############################################################
    ## Read data
    ###############################################################
    trace_obj = Trace(blocksize)
    trace_obj.read(DATA_FOLDER+experiment_name)
    pages = trace_obj.get_request()
    num_pages = len(pages)

    unique_pages = trace_obj.unique_pages()
    
    if cache_size_per < 1:
        cache_size = int(round(unique_pages*cache_size_per))
    else :
        cache_size = int(cache_size_per)
    
    colors = ['y','b','r','k','g']
    color_id = 0
    labels = []
    max_column_height = 0
    
    print 'unique_pages = ', unique_pages
    print 'cache_size = ', cache_size
    
    data = []
    hit_rate = []
    print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("Name","Hit Ratio(%)", "Hit Count", "Total Request","Unique Pages", "Time") )
    labels = []
    ########################
    ## Plot internal state
    ########################
    ax = plt.subplot(2,1,1)
    ax.set_title('internal state')
    xlim1,xlim2 = 0,0
    for v in VERTICAL_LINES :
        plt.axvline(x=v,color='g')
    

    for name in algorithm :
        algo = GetAlgorithm(cache_size, name)
        win = cache_size*WINDOW_SIZE
        
        start = time.time()
        hits, part_hit_rate, hit_sum = algo.test_algorithm(pages, partition_size=cache_size*WINDOW_SIZE)
        end = time.time()
        
        lbl = algo.visualize(plt)
        
        if lbl is not None :
            labels = labels + lbl
#         temp = 1751
#         plt.axvline(x=temp,color='b')
#         plt.axvline(x=10000+temp,color='r')
#         data.append(part_hit_rate)
        temp = np.append(np.zeros(win), hit_sum[:-win])
        data.append(hit_sum-temp)
        hit_rate.append(round(100.0 * hits / num_pages,2))
        print("{:<20} {:<20} {:<20} {:<20} {:<20}  {:<20}".format(name, round(100.0 * hits / num_pages,2), hits, num_pages, trace_obj.unique_pages(), round(end-start,3)))

        sys.stdout.flush()
    ax.set_ylim(0,1)
#     ax.autoscale(axis='both')
    plt.xlabel('Time')
    plt.ylabel('Weight')
    plt.legend(handles=labels,fancybox=True, framealpha=0.5)
    data = np.array(data)
    print('=====================================================')

    #####################
    ## Plot performance #
    #####################
    ax = plt.subplot(2,1,2)
    #ax.set_title('file name: %s\n' % experiment_name)
    rows = data.shape[0]
    cols = data.shape[1]
    T = np.array(range(0,cols))
    
    for v in VERTICAL_LINES :
        plt.axvline(x=v,color='g')
    
    cnt = rows
    labels = []
#     ax.set_ylim(-.05,1.05)
    ax.set_xlim(0,cols)
    for i in range(0,rows):        
        upper = data[i,:]
        l, = plt.plot(T,upper,c=colors[i],label=algorithm[i],alpha=0.5,linewidth=(rows-i)*1)
        labels.append(l)

    hit_rate_text = 'algorithm:  hit-rate\n'
    for i in range(0, rows) :
        hit_rate_text += '%s:  %f\n' % (algorithm[i], hit_rate[i])
    ax.annotate(hit_rate_text,(0.05,ANNOTATION_HEIGHT),textcoords='axes fraction',alpha=1, size=12)
    
    plt.xlabel('Request Window Number')
    plt.ylabel('Hit Rate')
    plt.legend(handles=labels,fancybox=True, framealpha=0.5)

    
    outfilename =OUTPUT_FOLDER+experiment_name+'_'+str(cache_size)+'.jpeg' 
    
    print(outfilename)
    plt.savefig(outfilename)
#     plt.show()
