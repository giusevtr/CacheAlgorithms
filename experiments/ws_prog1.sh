#!/bin/bash

CACHE_SIZE=50
FILES=(ws_prog.txt)
ALGORITHMS=(LRU LFU ARC LaCReME_v2 LaCReME_context1)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
