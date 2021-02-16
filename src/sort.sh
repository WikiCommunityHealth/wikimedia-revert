#!/bin/bash

input_file=/home/gandelli/dev/venv/dataset/revisions.tsv
output_file=/home/gandelli/dev/venv/dataset/sorted.tsv.bz2

sort -t $'\t' -k25,25 $input_file | bzip2 -c > $output_file