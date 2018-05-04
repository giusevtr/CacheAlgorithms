#!/bin/bash

CACHE_SIZE=500
FILES=(LRU_LFUx4_5NoiseResult.txt)
ALGORITHMS=(LeCaR LeCaR_q)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
