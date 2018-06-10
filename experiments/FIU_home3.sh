#!/bin/bash

CACHE_SIZE=0.01
FILES=(madmax-110108-112108.5.blkparse)
ALGORITHMS=(lru lfu arc LaCReME)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
