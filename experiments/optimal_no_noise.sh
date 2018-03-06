#!/bin/bash

CACHE_SIZE=0.2
FILES=(LRU_LFU_NO_Noise.txt LFU_LRU_NO_Noise.txt)
ALGORITHMS=(LRU LFU ARC LaCReME)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done
