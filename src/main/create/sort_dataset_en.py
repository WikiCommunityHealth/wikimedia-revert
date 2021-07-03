import os
import bz2
import subprocess
import os
from datetime import datetime
import sys 
path = "/home/berretta/euber/wikiusers/datasets/whdt/2021-05/enwiki/"
files = os.listdir(path)



inizio = datetime.now()

output_file = f'/home/gandelli/dev/data/en/revisions.tsv'
sort_script = '/home/gandelli/dev/wikimedia-revert/src/bash/sort.sh'

output = open(output_file, "w")
i = 0
for f in files:
    dump_in = bz2.open(path+f, 'r')
    line = dump_in.readline()
    i+=1

    print('    ora inizio a togliere tutto tranne revert e revertati dell mese-anno ' +
         str(i)+ "  ", datetime.now()-inizio)

    while line != '':
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')
        
        if len(values) < 67:
            continue
        
        if values[1] != 'revision' :
            continue

        if values[64] == 'false' and values[67] == 'false':
            continue

        output.write(line + '\n')
    


    dump_in.close()

output.close()
print('    finito di filtrare ora inizio a sortare ', datetime.now()-inizio)
subprocess.call([sort_script, 'en'])
print('    sorted in ', datetime.now()-inizio)