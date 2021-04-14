#%%
import bz2
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
import os
from utils import utils
import shutil

contoedit = {}
dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'


def main():
    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()

    current_page = 0
    reverted_m = {} # all the users a user reverted 
    edit_count = {}
    pages_m = {}

    reverted_user = ''
    current_page_id = 0
    current_page = ''
    reverter_id = 0

    while line != '':
        # line = dump_in.readline().rstrip()[:-1]# for uncompressed
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        # i want only namespace 0 and no vandalism
        if line == '' or values[28] != '0':
            continue


        page_id = int(values[23])
        page_name   = values[25]
        user = values[6]
        user_edit_count = values[21]
        rev_id      = values[52]
        reverter    = values[65]
        is_reverted = values[64]


        if user_edit_count != '':
            edit_count[user] = int(user_edit_count)
        else:
            edit_count[user] = 0

        if page_id != current_page_id:
            #calcola m sulla pagina 
            
            pages_m[current_page] = utils.get_M(reverted_m, edit_count, current_page)

            
            #initialize new page 
            current_page_id = page_id
            current_page = page_name
            reverted_m = {}

        else:
            if rev_id == reverter_id: ##if the currect reverts the previous one
                reverted_m.setdefault(user, []).append(reverted_user)

            if is_reverted == 'true':
                reverter_id = reverter
                reverted_user = user
    return pages_m

# pass every time the edit count so it consider the edit count at the time of the revert



        
# %%
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))
pages_m = main()
ordinato = sorted(pages_m.items(), key=lambda k: k[1], reverse=True)[:20]
print(datetime.now() - inizio)

# %%
