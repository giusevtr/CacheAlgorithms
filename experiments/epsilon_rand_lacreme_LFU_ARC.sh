#!/bin/bash

CACHE_SIZE=(100 100)
FILES=(epsilon_lru_lfu.txt epsilon_lfu_lru.txt)
ALGORITHMS=(lru lfu arc lacreme_LFU_ARC)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE[i]}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

