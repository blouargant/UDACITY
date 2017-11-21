#!/bin/bash

INPUT=$1
# cat results.txt | sed -e "s/  */ /g" | cut -d" " -f4,5,6,7
LINES=$(cat $INPUT | sed -e "s/  */ /g" | sed -e "s/.*: //" | sed -e "s/\%//g" | sed -e "s/ /;/g")

SCORE1="0"
SCORE2="0"
SCORE3="0"
SCORE4="0"
NBLINES=0
for line in $LINES; do
	NBLINES=$((NBLINES + 1))
	SCORE1="$SCORE1+$(echo $line | cut -d";" -f1)"
	SCORE2="$SCORE2+$(echo $line | cut -d";" -f2)"
	SCORE3="$SCORE3+$(echo $line | cut -d";" -f3)"
	SCORE4="$SCORE4+$(echo $line | cut -d";" -f4)"
done

echo $NBLINES
SCORE1=$(echo "($SCORE1)/$NBLINES" | bc)
SCORE2=$(echo "($SCORE2)/$NBLINES" | bc)
SCORE3=$(echo "($SCORE3)/$NBLINES" | bc)
SCORE4=$(echo "($SCORE4)/$NBLINES" | bc)

echo "Score 1: $SCORE1"
echo "Score 2: $SCORE2"
echo "Score 3: $SCORE3"
echo "Score 4: $SCORE4"
