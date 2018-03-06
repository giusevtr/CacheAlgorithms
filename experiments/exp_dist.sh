#!/bin/bash

CACHE_SIZE=0.2
FILES=(exp_dist_lru_lfu.txt exp_dist_lfu_lru.txt)
ALGORITHMS=(lru lfu lacreme)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

