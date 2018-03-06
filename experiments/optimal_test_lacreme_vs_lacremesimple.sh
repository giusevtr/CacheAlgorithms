#!/bin/bash

CACHE_SIZE=0.7
FILES=(LFU_LRU_LFU_LRU.txt LRU_LFU_LRU_LFU.txt)
ALGORITHMS=(lacreme lacreme_simple)

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done
