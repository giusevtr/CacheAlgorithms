#!/bin/bash

CACHE_SIZE=0.2
FILES=(madmax-110108-112108.1.blkparse madmax-110108-112108.3.blkparse madmax-110108-112108.4.blkparse madmax-110108-112108.5.blkparse)
ALGORITHMS=(lru lfu arc lacreme)

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done
