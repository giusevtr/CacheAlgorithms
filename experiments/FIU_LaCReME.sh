#!/bin/bash

CACHE_SIZE=0.2
FILES=(ikki-110108-112108.17.blkparse ikki-110108-112108.18.blkparse ikki-110108-112108.19.blkparse ikki-110108-112108.20.blkparse)
ALGORITHMS=(lru lfu arc lacreme)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
