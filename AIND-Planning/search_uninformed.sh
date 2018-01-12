#!/bin/bash

rm -f uninformed_results.txt

for P in 1 2 3; do
	echo "##################### PROBLEM $P #####################" >> uninformed_results.txt
	for T in 1 2 3 4 5 6 7; do
		echo "# TEST $T" >> uninformed_results.txt
		timeout 600s python run_search.py -p $P -s $T >> uninformed_results.txt
	done
done
