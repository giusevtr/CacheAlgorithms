#!/bin/bash
CACHE_SIZE=0.05
FILES=(casa2.blkparse)
ALGORITHMS=(lru lfu arc lacreme)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
