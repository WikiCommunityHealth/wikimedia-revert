#%% compute bymonth reverts 
import bz2
import subprocess
import os
from datetime import datetime
from utils import utils

dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'

output_file = '/home/gandelli/dev/data/monthly/pages/reverts.tsv'


dump_in = bz2.open(dataset, 'r')
output = open(output_file, "w")
line = dump_in.readline()

current_yearmonth = 'carlo'
current_page_id = ''
current_page = 0
nrev_monthly = 0
nrev_tot = 0
nvandalism = 0

inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))

while line != '':
    line = dump_in.readline().rstrip().decode('utf-8')[:-1]
    values = line.split('\t')
    if len(values) < 2:
        continue

    # i want only namespace 0 and no vandalism
    if line == '' or values[28] != '0' :
        continue

    if utils.is_vandalism(values[4]):
        nvandalism+=1
        continue

    timestamp = datetime.strptime(values[3],'%Y-%m-%d %H:%M:%S.%f')
    year_month = str(timestamp.year)+'-'+str(timestamp.month)
    page = values[24]
    page_id = values[23]
    
    nrev_monthly += 1
    nrev_tot +=1

    if current_page_id != page_id: #page finished 

        save(current_page,current_page_id,current_yearmonth, nrev_monthly, nvandalism)
    
        nrev_tot = 0
        nrev_monthly = 0
        nvandalism = 0
        current_page_id = page_id
        current_page = page
    else:
  
        if current_yearmonth != year_month:
            current_yearmonth = year_month
            save(page,page_id,year_month, nrev_monthly, nvandalism)
            nrev_monthly = 0
            nvandalism = 0

    

dump_in.close()

print(datetime.now() - inizio)



#%%

def save(page, page_id, year_month, nrev_monthly, nvandalism):
    output.write(f'{page}\t {page_id}\t {year_month}\t {nrev_monthly}\t {nvandalism}\n')


    

# %%
