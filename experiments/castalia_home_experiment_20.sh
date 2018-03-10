#!/bin/bash

CACHE_SIZE=0.2
FILES=(casa-110108-112108.3.blkparse ikki-110108-112108.3.blkparse madmax-110108-112108.3.blkparse topgun-110108-112108.3.blkparse)
ALGORITHMS=(LRU LFU ARC LaCReME_v2 OLCR OLCR_RAND)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
