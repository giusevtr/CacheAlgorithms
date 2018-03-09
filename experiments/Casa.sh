#!/bin/bash

CACHE_SIZE=0.05
FILES=(topgun-110108-112108.1.blkparse)
ALGORITHMS=(LRU LFU ARC)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
