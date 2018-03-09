#!/bin/bash

CACHE_SIZE=1000
FILES=(New_Exp_LRU_ARC_001Result.txt New_Exp_ARC_LRU_002Result.txt New_Exp_LFU_ARC_003Result.txt New_Exp_ARC_LFU_004Result.txt)
ALGORITHMS=(LRU LFU ARC LaCReME_v2)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
