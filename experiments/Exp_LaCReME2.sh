#!/bin/bash

CACHE_SIZE=1000
FILES=(Exp_0001Result.txt)
ALGORITHMS=(lru lfu arc LaCReME_v2)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
