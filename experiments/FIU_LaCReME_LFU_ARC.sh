#!/bin/bash

CACHE_SIZE=0.2
FILES=(ikki-110108-112108.11.blkparse ikki-110108-112108.12.blkparse ikki-110108-112108.13.blkparse ikki-110108-112108.14.blkparse)
ALGORITHMS=(lfu arc lacreme_LFU_ARC)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done
