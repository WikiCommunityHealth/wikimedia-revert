
import bz2
import subprocess
import os
from datetime import datetime

inizio = datetime.now()

dataset_folder = '/home/gandelli/dev/venv/dataset/italian/';
output_file = '/home/gandelli/dev/venv/dataset/revisions.tsv';

sort_script = '/home/gandelli/dev/venv/wikimedia-revert/src/bash/sort.sh';

output = open(output_file, "w")

for year in range(2001, 2021):

    dump_in = bz2.open(dataset_folder+'/it'+ str(year) +'.tsv.bz2', 'r')
    line = dump_in.readline()

    print('ora inizio a togliere tutto tranne revert e revertati dell anno'+ str(year)+ "  ", datetime.now()-inizio)
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
    dump_in.close()



output.close()
print('finito di filtrare ora inizio a sortare ', datetime.now()-inizio)
subprocess.call(sort_script)
print('sorted in ', datetime.now()-inizio)

os.remove(output_file)


