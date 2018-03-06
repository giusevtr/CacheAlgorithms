#!/bin/bash

CACHE_SIZE=0.2
FILES=(epsilon_lru_lfu.txt)
ALGORITHMS=(cexp_fa)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
