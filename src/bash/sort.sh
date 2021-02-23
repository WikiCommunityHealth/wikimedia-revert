#!/bin/bash

input_file=/home/gandelli/dev/data/revisions.tsv
output_file=/home/gandelli/dev/data/it/filtered_sorted_it.tsv.bz2

sort -t $'\t' -k25,25 $input_file | bzip2 -c > $output_file