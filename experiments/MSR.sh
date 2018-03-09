#!/bin/bash

CACHE_SIZE=50
FILES=(msr-cambridge1-sample.csv)
ALGORITHMS=(LRU LFU ARC)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
