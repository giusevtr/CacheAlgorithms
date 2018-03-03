#!/bin/bash

CACHE_SIZE=(50 50)
FILES=(epsilon_lru_lfu.txt epsilon_lfu_lru.txt)
ALGORITHMS=(lacreme lacreme_simple)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE[i]}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

