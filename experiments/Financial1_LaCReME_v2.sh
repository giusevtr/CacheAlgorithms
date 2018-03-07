#!/bin/bash

CACHE_SIZE=0.1
FILES=(Financial1_50K.spc)
ALGORITHMS=(LaCReME LaCReME_v2)
BLOCKSIZE=512

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
done
