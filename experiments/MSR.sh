#!/bin/bash

CACHE_SIZE=0.1
FILES=(msr-cambridge1-sample.csv)
ALGORITHMS=(LRU LFU ARC LaCReME)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
