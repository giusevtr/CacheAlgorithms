import sys
import time
from algorithms.GetAlgorithm import GetAlgorithm
from lib.traces import Trace
import warnings
import itertools
import matplotlib.pyplot as plt
import numpy as np
warnings.filterwarnings("ignore")

##
## python cache_size experiment_name algorithms
##

ANNOTATION_HEIGHT =0.7
IMAGE_FOLDER='output/'



def test_algorithm(algo, pages,  partition_size = 10) :
    hits = 0
    last_percent = -1
    num_pages = len(pages)

    partition_hit_rate = []
    hit_sum = []

    # print ''
    for i,p in enumerate(pages) :
        
        if p in algo :
            hits += 1
        
        algo.request(p)

        hit_sum.append(hits)

        ## Progres
        percent = int ((100.0 * (i+1) / num_pages))
        if percent != last_percent and percent % 10 == 0 :
            # print percent
            bars = int(percent / 10)
            sys.stdout.write('|')
            for i in range(bars) :
                sys.stdout.write('=')
            for i in range(10 - bars ) :
                sys.stdout.write(' ')
            sys.stdout.write('|\r')
            sys.stdout.flush()
            last_percent = percent

    for i in range(15 ) :
        sys.stdout.write(' ')
    sys.stdout.write('\r')
    sys.stdout.flush()
    return hits,partition_hit_rate,hit_sum


def run(param, ax_weight, ax_hitrate):
    assert "input_data_location" in param, "Error: parameter 'input_data_location' was not found"
    assert "experiment_name" in param, "Error: parameter 'experiment_name' was not found"
    assert "cache_size" in param, "Error: parameter 'cache_size' was not found"
    assert "algorithm" in param, "Error: parameter 'algorithm' was not found"
    
    ###########################################################################
    ## Specify input folder
    ## Create a file input_data_location.txt and put in the config folder
    ###########################################################################
    DATA_FOLDER = param["input_data_location"]
    experiment_name = param['experiment_name']
        
    ###############################################################
    ## Read data
    ###############################################################
    trace_obj = Trace(512)
    trace_obj.read(DATA_FOLDER+experiment_name)
    pages = trace_obj.get_request()
    pages = pages[:int(param['trace_limit'])] if 'trace_limit' in param else pages
    
    num_pages = len(pages)
    unique_pages = trace_obj.unique_pages()
    cache_size_per = float(param['cache_size'])
    param['cache_size'] = int(round(unique_pages*cache_size_per)) if cache_size_per < 1 else int(cache_size_per)
    
    ###############################################################
    ## Simulate algorithm
    ###############################################################
    algo = GetAlgorithm(param['algorithm'])(param)
        
    averaging_window_size = int(0.01*len(pages))
    start = time.time()
    hits, _, hit_sum = test_algorithm(algo, pages, partition_size=averaging_window_size)
    end = time.time()

    ###############################################################
    ## Visualize 
    ###############################################################
    visualize = 'visualize' in param and bool(param['visualize'])
    if visualize :
        
        for v in trace_obj.vertical_lines :
            ax_hitrate.axvline(x=v,color='g',alpha=0.75)
            ax_weight.axvline(x=v,color='g',alpha=0.75)
            
        
        
        temp = np.append(np.zeros(averaging_window_size), hit_sum[:-averaging_window_size])
        hitrate = (hit_sum-temp) / averaging_window_size
        
        ax_hitrate.set_xlim(0, len(hitrate))
        
        ax_hitrate.plot(range(len(hitrate)), hitrate,label=param['algorithm'], alpha=0.8)
        algo.visualize(ax_weight)
    
    del pages[:]
        
    return round(100.0 * hits / num_pages,2),  round(end-start,3)



def run_experiment(keys, values, exp_num = 1):
    ax_weight = plt.subplot(2,1,1)
    ax_hitrate = plt.subplot(2,1,2)
    
    for vals in itertools.product(*tuple(values)):
        param = {}
        parameters = "" 
        for k, v in zip(keys, vals) :
            parameters += "{:<20}".format(v[-20:])
            param[k] = v
        
        hit_rate, duration = run(param, ax_weight, ax_hitrate)
        parameters += "{:<20}".format(hit_rate)
        parameters += " : {:<10}".format(duration)
        
        print(parameters)
    

    ax_weight.set_ylim(-0.05,1.05)
    ax_weight.set_ylabel('Weight')

    ax_hitrate.set_ylim(-0.05,1.05)        
    ax_hitrate.set_xlabel('Time')
    ax_hitrate.set_ylabel('hit-rate')
    
    plt.legend(fancybox=True, framealpha=0.5)
    
    plt.savefig("output/%s_%d.png" % (sys.argv[config_idx], exp_num))
    
    plt.clf()

if __name__ == "__main__" :
    
    for config_idx in range(1, len(sys.argv)):
    
        config_file = open(sys.argv[config_idx], 'r')
        
        
        keys = []
        values = []
        header = ""
        exp_cnt = 1
        for line in config_file:
            if line.strip() == "":
                header += "{:<20}".format("hit rate")
                print(header)
                run_experiment(keys, values, exp_cnt)
                exp_cnt += 1
                del keys[:]
                del values[:]
                header = ""
                print("\n\n")
                continue
            key, vals = line.strip().split(":")
            keys.append(key)
            values.append(vals.split(","))
            header += "{:<20}".format(key[-18:])
        
        if len(values)>0:
            header += "{:<20}".format("hit rate")
            print(header)
            run_experiment(keys, values, exp_cnt)
        
                
#         print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("Name","Hit Ratio(%)", "Hit Count", "Total Request","Unique Pages", "Time") )
#         print("\n")
