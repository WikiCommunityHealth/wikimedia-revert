#%%
import bz2
import subprocess

from datetime import datetime

dump_in = open('/Users/alessiogandelli/wikipedia/lombardo.tsv', 'r')
line = dump_in.readline()
inizio = datetime.now()

output = open("data/revisions.tsv", "w")


input_file = "./data/revisions.tsv"
output_file = "./data/sorted.tsv"
prova2 = ["sort", "-t\t", "-k24", input_file, "-o", output_file ]

print('ora inizio a filtrare')
while line != '':
    line = dump_in.readline().rstrip()[:-1]
    values = line.split('\t')
    if len(values) < 2:
        continue

    if values[1] != 'revision':
        continue
    
    output.write(line + '\n')

output.close()
print('finito di filtrare ora inizio a sortare ')
print(datetime.now()-inizio)
process = subprocess.Popen(prova2).wait()


print('sortato')
print(datetime.now()-inizio)
# %%
