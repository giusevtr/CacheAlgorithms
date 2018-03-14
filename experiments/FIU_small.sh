#!/bin/bash

CACHE_SIZE=0.05
FILES=(casa5.1_80000.blkparse)
ALGORITHMS=(LRU LFU ARC LaCReME)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
