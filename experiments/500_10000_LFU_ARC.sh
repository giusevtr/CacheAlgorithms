#!/bin/bash

CACHE_SIZE=500
FILES=(10000_LFU_ARCx10Result.txt)
ALGORITHMS=(lru lfu arc LaCReMe)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
