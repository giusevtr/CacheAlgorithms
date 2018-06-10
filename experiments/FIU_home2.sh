#!/bin/bash

CACHE_SIZE=0.001
FILES=(ikki-110108-112108.5.blkparse)
ALGORITHMS=(lru lfu arc LaCReMe)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
