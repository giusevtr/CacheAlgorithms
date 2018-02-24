#!/bin/bash

CACHE_SIZE=(500 500)
FILES=(LRU_LFU_NO_Noise.txt LFU_LRU_NO_Noise.txt)
ALGORITHMS=(lru lfu arc LaCrema)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE[i]}" "${FILES[i]}" "${ALGORITHMS[@]}"
done
