import sys
import time
from algorithms.GetAlgorithm import GetAlgorithm
from lib.traces import Trace
import warnings
import itertools
import matplotlib.pyplot as plt
import numpy as np
warnings.filterwarnings("ignore")
import csv
from matplotlib.ticker import FuncFormatter

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

def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.0fK' % (x*1e-3)

def run(param, ax_weight, ax_hoarding, ax_hitrate):
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
            ax_hoarding.axvline(x=v,color='g',alpha=0.75)
            
        
        
        temp = np.append(np.zeros(averaging_window_size), hit_sum[:-averaging_window_size])
        hitrate = (hit_sum-temp) / averaging_window_size
        
        ax_hitrate.set_xlim(0, len(hitrate))
        
        ax_hitrate.plot(range(len(hitrate)), hitrate,label=param['algorithm'], alpha=0.8)
        algo.visualize(ax_weight,ax_hoarding, averaging_window_size)
    
    del pages[:]
        
    return round(100.0 * hits / num_pages,2),  round(end-start,3)



def run_experiment(keys, values, exp_num = 1):

    filename= values[1][0].strip().split("-")[0]
    
    with open('output/'+filename+'_hitrates.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        algo_names = []
        hit_rates =[]
        exp_names =[]
        ax_hitrate = plt.subplot2grid((5,1), (4,0))
        ax_weight = []
        
        formatter = FuncFormatter(millions)



        index_count = 0
        i=0
        for vals in itertools.product(*tuple(values)):
            
            ax_weight.append(plt.subplot2grid((5,1), (index_count,0)))
            ax_weight.append(plt.subplot2grid((5,1), (index_count+1, 0),sharex = ax_weight[i]))
            ax_weight[i].xaxis.set_major_formatter(formatter)
            ax_weight[i+1].xaxis.set_major_formatter(formatter)


            param = {}
            parameters = "" 
            for k, v in zip(keys, vals) :
                parameters += "{:<20}".format(v[-20:].strip())
                param[k] = v
            algo_names.append(param['algorithm'])
            exp_names.append(param['experiment_name'])
            hit_rate, duration = run(param, ax_weight[i],ax_weight[i+1], ax_hitrate)
            parameters += "{:<20}".format(hit_rate)
            parameters += " : {:<10}".format(duration)
            
            hit_rates.append(hit_rate)
            print(parameters)

            
        

            ax_weight[i].set_ylim(0,1.05)
            ax_weight[i].set_ylabel('Weight')
            ax_weight[i+1].set_title(param['algorithm'])
            index_count +=2
            i+= 2

        ax_hitrate.set_ylim(-0.05,1.05)        
        ax_hitrate.set_xlabel('Time')
        ax_hitrate.set_ylabel('hit-rate')
	#ax_hoarding.set_ylabel('hoarding')
        # plt.subplots_adjust(hspace= 0.5)
        
        
        plt.legend(fancybox=True, framealpha=0.5, loc=" upper right")
        plt.tight_layout()
        plt.savefig("output/%s_%s_%s.png" % (sys.argv[config_idx],  param['experiment_name'],param['algorithm']))
        
        plt.clf()
        spamwriter.writerow(algo_names[0:len(values[6])])
        for i in range (0,len(hit_rates),len(values[6])):

            spamwriter.writerow(hit_rates[i:i+len(values[6])])

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
            values.append(vals.strip().split(","))
            header += "{:<20}".format(key[-18:])
        
        if len(values)>0:
            header += "{:<20}".format("hit rate")
            print(header)
            run_experiment(keys, values, exp_cnt)
        
                
#         print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("Name","Hit Ratio(%)", "Hit Count", "Total Request","Unique Pages", "Time") )
#         print("\n")
