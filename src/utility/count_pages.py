import bz2
import subprocess
import os
from datetime import datetime

inizio = datetime.now()

dataset_folder = '/home/gandelli/dev/data/it/'


totali = set()
revisioni = set()
revert = set()

for year in range(2001, 2021):

    dump_in = bz2.open(dataset_folder+'/it' + str(year) + '.tsv.bz2', 'r')
    line = dump_in.readline()
    print(year)

    while line != '':
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')
        if len(values) < 2:
            continue
        if values[23] != '':
            page = int(values[23])

        totali.add(page)

        if values[1] == 'revision':
            revisioni.add(page)
        
            if values[64] == 'true' and values[67] == 'true':
                revert.add(page)



print('total page ', len(revisioni), len(totali))
print('with reverts', len(revert))