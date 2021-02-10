#!/bin/bash
#sort ../data/prove.tsv > bz2 > ../data/sortatoprova.tsv.bz2
input_file=data/revisions.tsv
output_file=data/sorted.tsv.bz2

sort -t\t -k24 $input_file > bz2 > $output_file