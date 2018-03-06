#!/bin/bash

CACHE_SIZE=0.2
FILES=(casa-110108-112108.5.blkparse casa-110108-112108.6.blkparse casa-110108-112108.7.blkparse casa-110108-112108.8.blkparse)
ALGORITHMS=(lru lfu arc LaCReMe LaCReME_context1)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

