
import bz2
import subprocess
import os
from datetime import datetime


dataset = '/home/gandelli/dev/data/test/revision_not_sorted.tsv';
output_file = '/home/gandelli/dev/data/test/magalli.tsv'


dump_in = open(dataset, 'r')
output = open(output_file, "w")
line = dump_in.readline()

page_id = '2039135'
page_name = 'Giancarlo_Magalli'

  
while line != '':
    line = dump_in.readline().rstrip()[:-1]
    values = line.split('\t')
    if len(values) < 2:
        continue

    if values[1] != 'revision':
        continue

   
    if values[25] == page_name:
        print(line)
        output.write(line + '\n')

dump_in.close()