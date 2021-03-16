#%%
import bz2
import subprocess
import os
from datetime import datetime


dataset = '/home/gandelli/dev/data/it/filtered_sorted_it.tsv.bz2'
output_file = '/home/gandelli/dev/data/test/senza_colonne.tsv'

dump_in = bz2.open(dataset, 'r')
output = open(output_file, "w")

line = dump_in.readline()

columns = [3,4,5,6,7,8,9,10,11,12,13,17,18,20,21,22,23,24,25,26,27,28,32,33,34,52,53,54,57,58,59,64,65,66,67]
def parseRow(word_list):
    row = ''
    for i in range(len(word_list)):
        if i in columns:
            row += (word_list[i] +'\t')
    return row

while line != '':
    line = dump_in.readline().rstrip().decode('utf-8')[:-1]
    values = line.split('\t')
    if len(values) < 2:
        continue
    row = parseRow(values)
    output.write(row + '\n')


bz2.compress(open(output_file, 'rb').read())


    
# %%
