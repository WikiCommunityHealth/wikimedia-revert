#!/bin/bash
LANG=$1

input_file=/home/gandelli/dev/data/$LANG/revisions.tsv
output_file_pages=/home/gandelli/dev/data/$LANG/sorted_by_pages.tsv.bz2
output_file_tstamp=/home/gandelli/dev/data/$LANG/sorted_by_timestamp.tsv.bz2


#input_file=/home/gandelli/dev/data/it/revisions.tsv
#output_file_pages=/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2


#sort by pages 
sort -t $'\t' -k25,25 "$input_file" | bzip2 -c > "$output_file_pages"
#sort by timestamp 
sort -t $'\t' -k3,3 "$input_file" | bzip2 -c > "$output_file_tstamp"
