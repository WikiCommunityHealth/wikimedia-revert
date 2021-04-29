#from each file of the  dataset remove everything but reverted/reverter and then sort by page 
import bz2
import subprocess
import os
from datetime import datetime

inizio = datetime.now()

dataset_folder = '/home/gandelli/dev/data/it/'
output_file = '/home/gandelli/dev/data/test/abantutto.tsv'

output = open(output_file, "w")

for year in range(2001, 2021):

    dump_in = bz2.open(dataset_folder+'/it' + str(year) + '.tsv.bz2', 'r')
    line = dump_in.readline()

    print('ora inizio a togliere tutto tranne revert e revertati dell anno' +
          str(year) + "  ", datetime.now()-inizio)
    while line != '':
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')
        if len(values) < 2:
            continue
        
        if values[24] == 'Aban':
            output.write(line + '\n')

    dump_in.close()


output.close()
print('finito di filtrare ora inizio a sortare ', datetime.now()-inizio)
