#!/bin/bash

CACHE_SIZE=50
FILES=(workingset.txt)
ALGORITHMS=(LRU LFU ARC LaCReME_LFU_ARC)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
