#!/bin/bash

CACHE_SIZE=0.2
FILES=(Exp_0001Result.txt Exp_0002Result.txt Exp_0003Result.txt Exp_0004Result.txt Exp_0005Result.txt Exp_0006Result.txt)
ALGORITHMS=(lru lfu arc Lacreme)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
