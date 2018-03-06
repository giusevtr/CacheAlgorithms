#!/bin/bash

CACHE_SIZE=0.2
FILES=(Financial1_50K.spc)
ALGORITHMS=(lru lfu arc lacreme)

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

