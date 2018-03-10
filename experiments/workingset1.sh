#!/bin/bash

CACHE_SIZE=50
FILES=(ws_25.txt)
ALGORITHMS=(OLCR LRU LFU ARC LaCReME_v2 OLCR_RAND)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
