#!/bin/bash

CACHE_SIZE=0.2
FILES=(Financial1_50K.spc)
ALGORITHMS=(arc LaCReME_context1)

for ((i=0;i<${#CACHE_SIZE[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${ALGORITHMS[@]}"
done

