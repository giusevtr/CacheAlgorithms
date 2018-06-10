import sys
import os
import time
import numpy as np
from algorithms.GetAlgorithm import GetAlgorithm
from lib.traces import Trace
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

##
## python cache_size experiment_name algorithms
##

ANNOTATION_HEIGHT =0.7
IMAGE_FOLDER='output/'
    
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
    OUTPUT_CONFIG_FILE = 'config/output_data_location.txt'
    
    ###########################################################################
    ## Specify input folder
    ## Create a file input_data_location.txt and put in the config folder
    ###########################################################################
    if os.path.isfile(INPUT_CONFIG_FILE) :
        f = open(INPUT_CONFIG_FILE, 'r')
        DATA_FOLDER = f.readline().rstrip('\n\r')
    else:
        print('%s not found')
        sys.exit(0)
    
    ###########################################################################
    ## Specify output location
    ## Create a file output_data_location.txt and put in the config folder
    ## This file should contain the path where the outputs will be saved
    ###########################################################################
    if os.path.isfile(OUTPUT_CONFIG_FILE) :
        f = open(OUTPUT_CONFIG_FILE, 'r')
        OUTPUT_FOLDER = f.readline().rstrip('\n\r')
    else:
        print('No output file found! No csv file will be generated. Create file config/output_data_location.txt. to get the output data')
        OUTPUT_FOLDER = None
    
    if len(sys.argv) <= 4 :
        print('Must provide more than 3 arguments')
        sys.exit(0)

    assert float(sys.argv[1]) > 0,  'cache_size must be positive'
    
    cache_size_per = float(sys.argv[1])
    experiment_name = sys.argv[2]
    blocksize = int(sys.argv[3])
    algorithm = sys.argv[4:]
    
    visualizeInternalStatePlot = True #experiment_name.endswith('.txt')
    
    
    ###############################################################
    ## Save data here
    ###############################################################
    data_dict = {}
    
    ###############################################################
    ## Plot title
    ###############################################################
    
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
        cache_size_label =  str(float(cache_size_per))
    else :
        cache_size = int(cache_size_per)
        cache_size_label = str(cache_size)
    
    averaging_window_size = int(0.01*len(pages))
    print 'averaging_window_size = ', averaging_window_size
    
    colors = ['y','b','r','k','g', 'c', 'm']
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
    
    if visualizeInternalStatePlot :
        ax = plt.subplot(2,1,1)
    else :
        ax = plt.subplot(1,1,1)
    
    #########################
    ## Plot vertical lines
    #########################
#     ax.set_title('%s:%s\n' % (experiment_name,cache_size_label))
    xlim1,xlim2 = 0,0
    for v in trace_obj.vertical_lines :
        plt.axvline(x=v,color='g',alpha=0.75)
    
    i = 0
    summary = 'name\thit rate\thits\tunique\tnumber of pages'
    algorithms_used = ''
    for name in algorithm :
        algo = GetAlgorithm(cache_size, name, visualization = visualizeInternalStatePlot)
        
        start = time.time()
        hits, part_hit_rate, hit_sum = algo.test_algorithm(pages, partition_size=averaging_window_size)
        end = time.time()
        
        stat = algo.getStats()
        if stat is not None:
            for attr in stat :
                data_dict['%s_%s' % (name, attr)] = stat[attr]
        
        if visualizeInternalStatePlot:
            lbl = algo.visualize(plt)
            data_dict['%s_weights' % name] = algo.getWeights()
        else :
            lbl = []
        i += 1
        
        if lbl is not None :
            labels = labels + lbl
        temp = np.append(np.zeros(averaging_window_size), hit_sum[:-averaging_window_size])
        data.append(hit_sum-temp)
        hit_rate.append(round(100.0 * hits / num_pages,2))
        
        ##################
        ## Store raw data
        ##################
        temp = [name] + hit_sum
        data_dict['%s_hits' % name] = hit_sum 
        algorithms_used += name if algorithms_used == "" else ':'+name
        
        
        hr = round(100.0 * hits / num_pages,2)
        hi = hits
        nu = num_pages
        un = trace_obj.unique_pages()
        ti = round(end-start,3)
        
        result = "{:<20} {:<20} {:<20} {:<20} {:<20}  {:<20}".format(name, round(100.0 * hits / num_pages,2), hits, num_pages, trace_obj.unique_pages(), round(end-start,3))
        print(result)
        summary += '%s\t%.2f\t%d\t%d\t%d\n' % (name,hr, hi, un, nu)

        sys.stdout.flush()
    ax.set_ylim(-0.05,1.05)
    plt.xlabel('Time')
    plt.ylabel('Weight')
    plt.legend(handles=labels,fancybox=True, framealpha=0.5)
#    plt.legend(handles=labels,fancybox=True, framealpha=0.5,fontsize=10,loc='center left', bbox_to_anchor=(1.1, 0.5))
    data = np.array(data)
#     plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    
    
    print('=====================================================')

    #####################
    ## Plot performance #
    #####################
    if visualizeInternalStatePlot:
        ax = plt.subplot(2,1,2)
    else :
        ax = plt.subplot(1,1,1)
        
    #ax.set_title('file name: %s\n' % experiment_name)
    rows = data.shape[0]
    cols = data.shape[1]
    T = np.array(range(0,cols))
    
    for v in trace_obj.vertical_lines :
        plt.axvline(x=v,color='g',alpha=0.75)
    
    cnt = rows
    labels = []
    ax.set_ylim(-.15,1.05)
    ax.set_xlim(0,cols)
    for i in range(0,rows):        
        hitrate = data[i,:] / (averaging_window_size)
        
        data_dict['%s_hits' % algorithm[i]] = np.array([T, data[i,:]]) .T
        data_dict['%s_hit_rate' % algorithm[i]] = np.array([T, hitrate]).T
        
        lbl = "%s" % (algorithm[i])
        l, = plt.plot(T,hitrate,c=colors[i],label=lbl,alpha=0.8,linewidth=(rows-i)*1.5)
        labels.append(l)

    hit_rate_text = ''
    for i in range(0, rows) :
        hit_rate_text += '%s:  %.2f\n' % (algorithm[i], hit_rate[i])
#     temp = ax.annotate(hit_rate_text,(0.01,0.8),textcoords='axes fraction',alpha=1, size=8, weight='bold', backgroundcolor='w')
    temp = ax.annotate(hit_rate_text,(1.055,0.7),textcoords='axes fraction',alpha=1, size=10, weight='bold', backgroundcolor='w')
    
    plt.xlabel('Requests')
#     plt.ylabel('Hit Rate (Window size = %d)' % averaging_window_size)
    plt.ylabel('Hit Rate')
#     plt.legend(handles=labels,fancybox=True, framealpha=0.5)
    plt.legend(handles=labels,fancybox=True, framealpha=0.5,loc='center left', fontsize=10, bbox_to_anchor=(1.1, 0.5))
    
    #####################################################################################################################################################################
    #####################################################################################################################################################################
    #####################################################################################################################################################################
    
    
    plt.subplots_adjust(left=0.1, right =0.82)
    
            
    ######################
    ## Save image
    #######################
    imagefilename = IMAGE_FOLDER + '%s_%s_%s.png' % (experiment_name,cache_size_label,algorithms_used) 
    print 'Saving graph image ', imagefilename
    plt.savefig(imagefilename)
    
    ######################
    ## Save data arrays
    #######################
    if OUTPUT_FOLDER is not None:
        for key in data_dict :
            outfilename =  OUTPUT_FOLDER + "%s_%s_%s.npy" %(key, experiment_name, cache_size_label)
            print 'Saving %s' % outfilename
            np.save(outfilename, data_dict[key])
    
    ######################
    ## Save summary
    #######################
    if OUTPUT_FOLDER is not None:
        summaryfilename =  OUTPUT_FOLDER + "summary_%s_%s_%s.txt" % (experiment_name, cache_size_label, algorithms_used)
        print 'Saving %s' % summaryfilename
        f = open(summaryfilename, 'w')
        f.write(summary)
        f.close()
    
