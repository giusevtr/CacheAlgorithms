#!/bin/bash

CACHE_SIZE=0.05
FILES=(CAMRESWMSA03-lvm1.csv)
ALGORITHMS=(lru lfu arc LaCReMe)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
