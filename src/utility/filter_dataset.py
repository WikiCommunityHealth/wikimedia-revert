#%% from all the dataset extract the raw rows that respect some conditions
import bz2
import subprocess
import os
from datetime import datetime


dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'

output_file = '/home/gandelli/dev/data/test/lisaAnn.tsv'


dump_in = bz2.open(dataset, 'r')
output = open(output_file, "w")
line = dump_in.readline()

page_id = '2039135'
page_name = 'Lisa_Ann'
stop = 'Ninetales'


massimo = 0 
minimo = 100000000
pagine = set()

stampa = False
  
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))

while line != '':
    line = dump_in.readline().rstrip().decode('utf-8')[:-1]
    values = line.split('\t')
    if len(values) < 2:
        continue

    if values[1] != 'revision':
        continue
    
   
    if values[25] == page_name:
        output.write(line + '\n')

dump_in.close()

print(datetime.now() - inizio)


# %%
