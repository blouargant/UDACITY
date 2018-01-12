#!/bin/bash

rm -f informed_results.txt

for P in 1 2 3; do
	echo "##################### PROBLEM $P #####################" >> informed_results.txt
	for T in 8 9 10; do
		echo "# TEST $T" >> informed_results.txt
		timeout 600s python run_search.py -p $P -s $T >> informed_results.txt
	done
done
