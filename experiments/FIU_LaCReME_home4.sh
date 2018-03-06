#!/bin/bash

CACHE_SIZE=0.2
FILES=(topgun-110108-112108.1.blkparse topgun-110108-112108.2.blkparse topgun-110108-112108.3.blkparse topgun-110108-112108.4.blkparse)
ALGORITHMS=(lru lfu arc lacreme)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done
