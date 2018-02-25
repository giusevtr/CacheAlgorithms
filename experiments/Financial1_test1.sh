#!/bin/bash

CACHE_SIZE=(2000)
FILES=(Financial1_50K.spc)
ALGORITHMS=(lru lfu arc LaCrema)


for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE[i]}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

