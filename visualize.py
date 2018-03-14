'''
Created on Mar 13, 2018

@author: giuseppe
'''
import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt


INPUT_CONFIG_FILE = 'experiments/config/input_data_location.txt'
OUTPUT_CONFIG_FILE = 'experiments/config/output_data_location.txt'

if os.path.isfile(OUTPUT_CONFIG_FILE) :
    f = open(OUTPUT_CONFIG_FILE, 'r')
    OUTPUT_FOLDER = f.readline().rstrip('\n\r')
else:
    print('No output file found! No csv file will be generated. Create file config/output_data_location.txt. to get the output data')
    OUTPUT_FOLDER = None
    
    
inputfile = sys.argv[1]
data = np.load(OUTPUT_FOLDER+inputfile)

print data


