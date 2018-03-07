#!/bin/bash

CACHE_SIZE=500
FILES=(Exp_0001Result.txt)
ALGORITHMS=(lru lfu arc lacreme_t1t2)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
