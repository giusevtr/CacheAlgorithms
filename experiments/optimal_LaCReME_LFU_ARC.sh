#!/bin/bash

CACHE_SIZE=0.7
FILES=(LRU_LFU_NO_Noise.txt LFU_LRU_NO_Noise.txt)
ALGORITHMS=(LRU ARC LaCReME_LFU_ARC)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
