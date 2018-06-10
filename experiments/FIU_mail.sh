#!/bin/bash

CACHE_SIZE=0.001
FILES=(cheetah.cs.fiu.edu-110108-113008.3.blkparse)
ALGORITHMS=(lru lfu arc LaCReME)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
