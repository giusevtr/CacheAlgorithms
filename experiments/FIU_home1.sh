#!/bin/bash

CACHE_SIZE=0.2
FILES=(casa-110108-112108.3.blkparse)
ALGORITHMS=(lru lfu arc LaCReMe)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
