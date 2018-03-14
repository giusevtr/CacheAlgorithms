#!/bin/bash

CACHE_SIZE=50
FILES=(ws_90x5.txt)
ALGORITHMS=(LRU LFU ARC LeCaR)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
