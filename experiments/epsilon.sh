#!/bin/bash

CACHE_SIZE=(50)
FILES=(epsilon_lru_lfu.txt)
ALGORITHMS=(LRU LFU LeCaR OLCR)
BLOCKSIZE=1

for ((cz=0;cz<${#CACHE_SIZE[@]};++cz)); do
	for ((i=0;i<${#FILES[@]};++i)); do
	    python ../run.py "${CACHE_SIZE[cz]}" "${FILES[i]}" "${BLOCKSIZE}" "${ALGORITHMS[@]}"
	done
done 