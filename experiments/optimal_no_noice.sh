#!/bin/bash

CACHE_SIZE=500
FILES='LRU_LFU_NO_Noise LFU_LRU_NO_Noise'
OUTOUT_FILE='output'


for f in ${FILES};
do
echo $f
python ../runexperiment2.py $CACHE_SIZE $f'.txt' $f lru lfu bandit_double_hist2
done
