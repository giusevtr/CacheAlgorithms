#!/bin/bash

CACHE_SIZE=(1090 5000)
FILES=(Financial1_50K.spc Financial1_300K.spc)
ALGORITHMS=(lru lfu LaCrema)


for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE[i]}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

