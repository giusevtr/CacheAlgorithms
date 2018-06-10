#!/bin/bash

CACHE_SIZE=0.10
FILES=(madmax6_80000-200000.blkparse)
ALGORITHMS=(lru lfu arc LaCReMe)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
