#!/bin/bash
set -e

dir=../data
for f in "$dir"/*
do
    if [[ $f == *.tsp ]]
    then
        for alg in Approx LS1 LS2;
        do
            ~/miniconda3/bin/python tsp_main.py -inst $f -alg $alg -time 100 -seed 1
        done
    fi
done
