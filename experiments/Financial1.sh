#!/bin/bash

CACHE_SIZE=(10 20)
FILES=(Financial1_small.spc Financial1_small.spc)
ALGORITHMS=(lru lfu)


for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE[i]}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

