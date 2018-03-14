#!/bin/bash

CACHE_SIZE=0.10
FILES=(casa5.2_10000.blkparse)
ALGORITHMS=(lru lfu arc LaCReME_v2)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
