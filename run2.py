import sys
import time
from algorithms.GetAlgorithm import GetAlgorithm
from lib.traces import Trace
import warnings
import itertools
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

    return hits,partition_hit_rate,hit_sum


def run(param):
    assert "input_data_location" in param, "Error: parameter 'input_data_location' was not found"
    assert "experiment_name" in param, "Error: parameter 'experiment_name' was not found"
    assert "cache_size" in param, "Error: parameter 'cache_size' was not found"
    assert "algorithm" in param, "Error: parameter 'algorithm' was not found"
    
    
    experiment_name = param['experiment_name']
    
    
    ###########################################################################
    ## Specify input folder
    ## Create a file input_data_location.txt and put in the config folder
    ###########################################################################
    DATA_FOLDER = param["input_data_location"]
    
    ###########################################################################
    ## Specify output location
    ## Create a file output_data_location.txt and put in the config folder
    ## This file should contain the path where the outputs will be saved
    ###########################################################################
    
    ###############################################################
    ## Read data
    ###############################################################
    trace_obj = Trace(512)
    trace_obj.read(DATA_FOLDER+experiment_name)
    pages = trace_obj.get_request()
    num_pages = len(pages)

    unique_pages = trace_obj.unique_pages()
    
    cache_size_per = float(param['cache_size'])
    if cache_size_per < 1:
        param['cache_size'] = int(round(unique_pages*cache_size_per))
    else :
        param['cache_size'] = int(cache_size_per)
    
    
    algo = GetAlgorithm(param['algorithm'])(param)
    
#     if algorithm.lower() == "lecar" :
#         if "learning_rate" in param:
#             algo.learning_rate = float(param['learning_rate'])
#         if "history_size" in param:
#             algo.history_size = float(param['history_size'])
    
    start = time.time()
    hits, part_hit_rate, hit_sum = test_algorithm(algo, pages, partition_size= int(0.01*len(pages)))
    end = time.time()
    
#     result = "{:<20} {:<20} {:<20} {:<20} {:<20}  {:<20}".format(algorithm, round(100.0 * hits / num_pages,2), hits, num_pages, trace_obj.unique_pages(), round(end-start,3))
#     print(result)
    sys.stdout.flush()
        
    return round(100.0 * hits / num_pages,2),  round(end-start,3)



if __name__ == "__main__" :
    config_file = open(sys.argv[1], 'r')
    
    keys = []
    values = []
    header = ""
    for line in config_file:
        if line.strip() == "":
            continue
        key, vals = line.strip().split(":")
        keys.append(key)
        values.append(vals.split(","))
        header += "{:<25}".format(key[-20:])
    
    header += "{:<25}".format("hit rate")
    
    print(header)
    
    for vals in itertools.product(*tuple(values)):
        param = {}
        parameters = "" 
        for k, v in zip(keys, vals) :
            parameters += "{:<25}".format(v[-20:])
#             print "== {:<25}".format(k,v)
            param[k] = v
        
        hit_rate, duration = run(param)
        parameters += "{:<25}".format(hit_rate)
        print(parameters)
#         print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("Name","Hit Ratio(%)", "Hit Count", "Total Request","Unique Pages", "Time") )
#         print("\n")
