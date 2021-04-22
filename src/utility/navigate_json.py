#%%
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

import json
from datetime import datetime
import numpy as np
import pandas as pd
from utils import utils 


dataset_folder_pages = '/home/gandelli/dev/data/wars_json/pages/'
reverts_df = []

def read_json(path):
    i = 10 # number of files in the wars folder
    #pages
    for i in range (0,i):
        dump_in = open(f"{path}wars_{i}.json")
        line = dump_in.readline()
        while(line != ''):
            line = dump_in.readline()
            if line == '{}]' or line == '':
                continue
            page = json.loads(line[:-2]) # it's called page but could be also an user 

            reverts_df.append((page['title'], page['n_reverts'],page['n_reverts_in_chains']))

read_json(dataset_folder_pages)
# %%
reverts_df = pd.DataFrame(reverts_df, columns=['title', 'n_reverts', 'n_reverts_in_chains'])

reverts_df['rapporto'] = reverts_df['n_reverts_in_chains'] / reverts_df['n_reverts']

# %%
