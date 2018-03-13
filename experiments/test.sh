#!/bin/bash

CACHE_SIZE=500
FILES=(500_10000_LFU_LRUx100Result.txt)
ALGORITHMS=(lru lfu arc LeCaR)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
