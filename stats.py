import sys
import time
from lib.traces import Trace
import warnings
import itertools
import numpy as np
warnings.filterwarnings("ignore")

##
## python cache_size experiment_name algorithms
##

ANNOTATION_HEIGHT =0.7
IMAGE_FOLDER='output/'


def run(param):
    assert "input_data_location" in param, "Error: parameter 'input_data_location' was not found"
    assert "experiment_name" in param, "Error: parameter 'experiment_name' was not found"
    assert "cache_size" in param, "Error: parameter 'cache_size' was not found"
    #assert "algorithm" in param, "Error: parameter 'algorithm' was not found"
    
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

    print("{:<40} {:<20} {:<20} ".format("Name", "Total Request","Unique Pages") )
    print("\n")
    print("{n:<40} {r:<20} {u:<20} ".format(n= experiment_name, r= num_pages, u=unique_pages) )
    
   



def run_experiment(keys, values, exp_num = 1):

    for vals in itertools.product(*tuple(values)):
        param = {}
        parameters = "" 
        for k, v in zip(keys, vals) :
            parameters += "{:<20}".format(v[-20:].strip())
            param[k] = v
        
        run(param)
        

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
                #print(header)
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
            #print(header)
            run_experiment(keys, values, exp_cnt)
        
                
        # print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("Name","Hit Ratio(%)", "Hit Count", "Total Request","Unique Pages", "Time") )
        # print("\n")
