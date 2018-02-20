#!/bin/bash


CACHE_SIZE=50
FILES='syncdata_40K_FR syncdata_40K_RF'


for f in $FILES;
do
#echo $f'.in'
python ../runexperiment2.py $CACHE_SIZE $f'.txt' $f lru lfu bandit_double_hist2
done


