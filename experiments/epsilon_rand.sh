#!/bin/bash

CACHE_SIZE=(50 50)
FILES=(epsilon_rand_lru_lfu.txt epsilon_rand_lfu_lru.txt)
ALGORITHMS=(lru lfu arc LaCrema)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE[i]}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

