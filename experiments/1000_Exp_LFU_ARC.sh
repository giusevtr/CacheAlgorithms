#!/bin/bash

CACHE_SIZE=1000
FILES=(1000_Exp_LFU_ARC_LFU_ARCResult.txt)
ALGORITHMS=(lru lfu arc LaCReMe)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
