#!/bin/bash

CACHE_SIZE=0.2
FILES=(ikki-110108-112108.9.blkparse ikki-110108-112108.10.blkparse ikki-110108-112108.11.blkparse ikki-110108-112108.12.blkparse)
ALGORITHMS=(lru lfu arc LaCReMe LaCReME_context1)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
