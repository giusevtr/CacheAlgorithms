#!/bin/bash

CACHE_SIZE=0.05
FILES=(topgun-110108-112108.1.blkparse topgun-110108-112108.2.blkparse topgun-110108-112108.3.blkparse topgun-110108-112108.4.blkparse topgun-110108-112108.5.blkparse topgun-110108-112108.6.blkparse)
ALGORITHMS=(lru lfu arc lacreme)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
