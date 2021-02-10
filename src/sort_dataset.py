#%%
import bz2
import subprocess
import os
from datetime import datetime

inizio = datetime.now()

dataset_path = '/Users/alessiogandelli/wikipedia/lombardo.tsv.bz2';
input_file = "./data/revisions.tsv"

output = open(input_file, "w")
dump_in = bz2.open(dataset_path, 'r')
line = dump_in.readline()


print('ora inizio a togliere tutto tranne revert e revertati')
while line != '':
    line = dump_in.readline().rstrip().decode('utf-8')[:-1]
    values = line.split('\t')
    if len(values) < 2:
        continue

    if values[1] != 'revision':
        continue
    
    if values[64] == 'false' and values[67] == 'false': 
        continue 

    
    output.write(line + '\n')

output.close()
dump_in.close()

print('finito di filtrare ora inizio a sortare ', datetime.now()-inizio)
subprocess.call('./src/sort.sh')
print('sorted in ', datetime.now()-inizio)


os.remove(input_file)

# %%
