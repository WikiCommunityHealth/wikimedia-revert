#%% from all the dataset extract the raw rows that respect some conditions
import bz2
import subprocess
import os
from datetime import datetime


dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'

output_file = '/home/gandelli/dev/data/test/chiocciola.tsv'


dump_in = bz2.open(dataset, 'r')
output = open(output_file, "w")
line = dump_in.readline()

page_id = '105152'
page_name = 'Ankogel_-_temp'
stop = 'Ninetales'
user = 'Ombra'

massimo = 0 
minimo = 100000000
pagine = set()

stampa = False
i = 50
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))

while line != '':
    line = dump_in.readline().rstrip().decode('utf-8')[:-1]
    values = line.split('\t')
    if len(values) < 2:
        continue

    if values[1] != 'revision':
        continue

 #   if  user == values[6]:
  #      output.write(line + '\n')
    #     print('eccolo')
    if values[23] == page_id :
    #     #i-=1
         output.write(line + '\n')
         print('eccolo')
   # elif i > 0:
      #  output.write(line + '\n')

   
        
    

dump_in.close()

print(datetime.now() - inizio)


# %%

# %%
