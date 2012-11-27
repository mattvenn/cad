#!/bin/bash
dest=~/Desktop/goboards
args="--noText --drawSizeLine"
for i in 9 13 19; do
    ./go.py $args --lines $i 
    mv board.svg $dest/$i.svg
done
