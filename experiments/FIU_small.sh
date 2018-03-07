#!/bin/bash

CACHE_SIZE=0.1
FILES=(FIU_traces.blkparse)
ALGORITHMS=(LRU ARC LaCReME)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
