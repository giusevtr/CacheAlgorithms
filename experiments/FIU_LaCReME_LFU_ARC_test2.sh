#!/bin/bash

CACHE_SIZE=0.2
FILES=(ikki-110108-112108.15.blkparse ikki-110108-112108.16.blkparse ikki-110108-112108.17.blkparse ikki-110108-112108.18.blkparse)
ALGORITHMS=(lru lfu arc lacreme_LFU_ARC)

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done
