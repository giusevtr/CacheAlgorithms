#!/bin/bash

CACHE_SIZE=(100)
FILES=(Financial1_50K.spc)
ALGORITHMS=(lru lfu_decay2 arc lacreme)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE[i]}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

