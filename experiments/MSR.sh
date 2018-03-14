#!/bin/bash

CACHE_SIZE=0.001
FILES=(CAM-02-SRV-lvm0.csv-80000.csv)
ALGORITHMS=(LRU LFU ARC LaCReME)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
