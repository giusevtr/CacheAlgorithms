#!/bin/bash

CACHE_SIZE=0.1
FILES=(ws_75x5.txt)
ALGORITHMS=(LRU LFU ARC LeCaR)
BLOCKSIZE=1

for ((i=0;i<${#FILES[@]};++i)); do
    python ../run.py "${CACHE_SIZE}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
	python  visualize.py "${FILES[i]}_${CACHE_SIZE}"
done



