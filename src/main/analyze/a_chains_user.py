#%% analyze the json pages about chains 
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime

inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))

# PAGE EXAMPLE
# {'title': 'Zuppa_di_pesce_(film)',
#  'chains': [{'revisions': ['95861493', '95861612', '95973728'],
#    'users': {'93.44.99.33': '', 'Kirk39': '63558', 'AttoBot': '482488'},
#    'len': 3,
#    'start': '2018-04-01 04:54:40.0',
#    'end': '2018-04-05 07:36:26.0'}],
#  'n_chains': 1,
#  'n_reverts': 3,
#  'mean': 3.0,
#  'longest': 3,
#  'M': 0,
#  'lunghezze': {'3': 1}}

output_folder = '/home/gandelli/dev/data/ita/chains/results/'

# read jsons file 
dataset_folder = '/home/gandelli/dev/data/ita/chains/user/'
i = 10 # number of files in the wars folder

pagine = 0



stats = []

serieA = {}
pino = {}
pages =[]

for i in range (0,i):
    dump_in = open(f"{dataset_folder}wars_{i}.json")
    line = dump_in.readline()
    while(line != ''):
        line = dump_in.readline()
        if line == '{}]' or line == '' or line == '{}]{}]':
            continue

        page = json.loads(line[:-2])
        
        stats.append({ 'user': page['user'],'n_chains': page['n_chains'],'mean' :page['mean'] ,'n_reverts': page['n_reverts'] ,'G':  page['G']})

        if page['user'] == 'CristianCantoro':
            serieA = page
        
        if page['user'] == 'Barcelona':
            pino = page

        reverts[page['user']] = page['longest']
        if page['user'] == 'CristianCantoro':
            for chain in page['chains']:
                pages.append({'user':page['user'], 'page': chain['page']})
                
        
        
print(datetime.now() - inizio)

# %%
df = pd.DataFrame(stats)
df = df.sort_values('n_reverts', ascending=False).head(15)
df

# %%
df = pd.DataFrame(pages)
df.groupby('page').count().sort_values('user', ascending=False).head(10)
# %%
