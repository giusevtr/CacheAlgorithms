#!/bin/bash

CACHE_SIZE=50
FILES=(epsilon_lru_lfu.txt)
ALGORITHMS=(LRU LFU LOMP)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
