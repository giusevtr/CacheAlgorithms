#!/bin/bash

CACHE_SIZE=500
FILES='LRU_LFU.txt'
OUTOUT_FILE='output'


for f in ${FILES};
do
echo $f
python ../runexperiment.py $CACHE_SIZE $f $OUTOUT_FILE lru lfu BANDIT
done


