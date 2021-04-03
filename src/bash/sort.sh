#!/bin/bash

input_file=/home/gandelli/dev/data/revisions.tsv
output_file_pages=/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2


#sort by pages 
sort -t $'\t' -k25,25 $input_file | bzip2 -c > $output_file_pages

