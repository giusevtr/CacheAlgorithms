#!/bin/bash

CACHE_SIZE=1000
FILES=(1000_Exp_ARC_LFU_ARC_LFUResult.txt)
ALGORITHMS=(LRU LFU ARC LaCReME LaCReME_v2)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
