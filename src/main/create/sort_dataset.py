#from each file of the  dataset remove everything but reverted/reverter and then sort by page 
import bz2
import subprocess
import os
from datetime import datetime
import sys 

language = sys.argv[1]

inizio = datetime.now()

dataset_folder = f'/home/gandelli/dev/data/dumps/{language}/'
output_file = f'/home/gandelli/dev/data/{language}/revisions.tsv'

sort_script = '/home/gandelli/dev/wikimedia-revert/src/bash/sort.sh'

output = open(output_file, "w")



for year in range(2001, 2021):

    dump_in = bz2.open(dataset_folder+language+ str(year) + '.tsv.bz2', 'r')
    line = dump_in.readline()
    

    print('    ora inizio a togliere tutto tranne revert e revertati dell anno ' +
          str(year) + "  ", datetime.now()-inizio)

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
subprocess.call([sort_script, language])
print('    sorted in ', datetime.now()-inizio)

#os.remove(output_file)
