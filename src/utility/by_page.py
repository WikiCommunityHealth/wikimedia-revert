#%% from all the dataset extract the raw rows that respect some conditions
import bz2
import subprocess
import os
from datetime import datetime
from utils import utils


dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'


dump_in = bz2.open(dataset, 'r')
line = dump_in.readline()

reverted_user = ''
current_page_id = 0
current_page = ''
reverter_id = 0

  
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))

while line != '':
    line = dump_in.readline().rstrip().decode('utf-8')[:-1]
    values = line.split('\t')
    if len(values) < 2:
        continue
    if line == '' or values[28] != '0' or utils.is_vandalism(values[4]):
            continue

    if values[1] != 'revision':
        continue

    page_id = int(values[23])
    page_name   = values[25]
    user = values[6]
    user_edit_count = values[21]
    rev_id      = values[52]
    reverter    = values[65]
    is_reverted = values[64]

    if page_id != current_page_id:
        #calcola m sulla pagina 
        print('processo current page che è finita', current_page)

        
        
        #initialize new page 
        current_page_id = page_id
        current_page = page_name
        reverted_m = {}


dump_in.close()

print(datetime.now() - inizio)
# %%
