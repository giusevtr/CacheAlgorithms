#!/bin/bash

CACHE_SIZE=0.01
FILES=(casa_100000.blkparse)
ALGORITHMS=(LaCReME_v2 LRU LFU ARC )
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
