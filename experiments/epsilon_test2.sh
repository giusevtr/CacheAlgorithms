#!/bin/bash

CACHE_SIZE=0.2
FILES=(epsilon_lru_lfu.txt)
ALGORITHMS=(cexp_fa)

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

