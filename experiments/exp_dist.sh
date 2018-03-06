#!/bin/bash

CACHE_SIZE=0.2
FILES=(exp_dist_lru_lfu.txt exp_dist_lfu_lru.txt)
ALGORITHMS=(lru lfu lacreme)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
