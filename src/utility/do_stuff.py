#%% from all the dataset extract the raw rows that respect some conditions
import bz2
import subprocess
import os
from datetime import datetime



dataset = '/home/gandelli/dev/data/test/lisaAnn.tsv'


dump_in = open(dataset, 'r')

line = dump_in.readline()



  
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))

while line != '':
    line = dump_in.readline().rstrip()[:-1]
    values = line.split('\t')
    if len(values) < 2:
        continue

    if values[1] != 'revision':
        continue
    
    user_id = values[5]
    username = values[7]
    edit_count = values[21]
    print(user_id, username, edit_count)

dump_in.close()

print(datetime.now() - inizio)


# %%
