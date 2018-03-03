#!/bin/bash

CACHE_SIZE=(500 500)
FILES=(LFU_LRU_LFU_LRU.txt LRU_LFU_LRU_LFU.txt)
ALGORITHMS=(LRU LFU ARC LaCReME)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE[i]}" "${FILES[i]}" "${ALGORITHMS[@]}"
done
