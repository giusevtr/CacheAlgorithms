#!/bin/bash

CACHE_SIZE=(50)
FILES=(epsilon_lru_lfu.txt)
ALGORITHMS=(cexp_fa)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE[i]}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

