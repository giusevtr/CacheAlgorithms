#!/bin/bash

CACHE_SIZE=0.001
FILES=(webresearch-030409-033109.3.blkparse)
ALGORITHMS=(lru lfu arc LaCReME)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
