#%%
import bz2
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
import os

import shutil


dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'

dump_in = bz2.open(dataset, 'r')
line = dump_in.readline()

current_page = 0
reverts = {} # all the users a user reverted 

reverted_user = ''
current_page_id = 0
reverter_id = 0

while line != '':
    # line = dump_in.readline().rstrip()[:-1]# for uncompressed
    line = dump_in.readline().rstrip().decode('utf-8')[:-1]
    values = line.split('\t')

    # i want only namespace 0 and no vandalism
    if line == '' or values[28] != '0':
        continue


    page_id = int(values[23])
    user = values[7]
    user_edit_count = values[21]
    rev_id      = values[52]
    reverter    = values[65]
    is_reverted = values[64]
    

    if page_id != current_page_id:
        #calcola m sulla pagina 
        get_M(reverts)
        #initialize new page 
        current_page_id = page_id
        reverts = {}

    else:
        if rev_id == reverter_id: ##if the currect reverts the previous one
            reverts.setdefault(user, []).append(reverted_user)

        if is_reverted == 'true':
            reverter_id = reverter
            reverted_user = user
  
# %%
def get_M(reverts):

    mutual = set()

    for user, reverted in reverts.items():
        for rev in reverted:
            if rev in reverts.keys():
                if user in reverts[rev]:
                    print(user, rev)
                    if user > rev:
                        mutual.add((user,rev))
                    elif user < rev:
                        mutual.add((rev,user))



        
# %%
