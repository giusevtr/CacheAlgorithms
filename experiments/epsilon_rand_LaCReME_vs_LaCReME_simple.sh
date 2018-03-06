#!/bin/bash

CACHE_SIZE=0.2
FILES=(epsilon_rand_lru_lfu.txt epsilon_rand_lfu_lru.txt)
ALGORITHMS=(arc lacreme LaCReME_simple)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

