#%%
import bz2
import subprocess
import os
from datetime import datetime


dataset = '/home/gandelli/dev/data/it/filtered_sorted_it.tsv.bz2'

output_file = '/home/gandelli/dev/data/test/demoni.tsv'


dump_in = bz2.open(dataset, 'r')
output = open(output_file, "w")
line = dump_in.readline()

page_id = '2039135'
page_name = 'Pino_Rauti'
stop = 'Ninetales'


massimo = 0 
minimo = 100000000
pagine = set()

stampa = False
  
while line != '':
    line = dump_in.readline().rstrip().decode('utf-8')[:-1]
    values = line.split('\t')
    if len(values) < 2:
        continue

    if values[1] != 'revision':
        continue
    
    pagine.add(int(values[23]))
    massimo = max(massimo, int(values[23]))
    minimo = min(minimo, int(values[23]))
   
    if values[25] == page_name:
        output.write(line + '\n')

dump_in.close()

len(pagine)
print(minimo, massimo)
# %%
