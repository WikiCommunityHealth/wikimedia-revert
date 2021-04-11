#%%
import bz2
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
import os

import shutil

contoedit = {}
dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'


def main():
    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()

    current_page = 0
    reverts = {} # all the users a user reverted 
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
            
            pages_m[current_page] = get_M(reverts, edit_count, current_page)

            
            #initialize new page 
            current_page_id = page_id
            current_page = page_name
            reverts = {}

        else:
            if rev_id == reverter_id: ##if the currect reverts the previous one
                reverts.setdefault(user, []).append(reverted_user)

            if is_reverted == 'true':
                reverter_id = reverter
                reverted_user = user
    return pages_m

#i pass every time the edit count so it consider the edit count at the time of the revert
def get_M(reverts, edit_count, page):

    mutual = set()

    for user, reverted in reverts.items():
        for rev in reverted:
            if rev in reverts.keys():
                if user in reverts[rev]:
                    if not is_bot(user) or not is_bot(rev):
                        if user > rev:              
                            mutual.add((user,rev))
                        elif user < rev:
                            mutual.add((rev,user))
    m = 0
    for couple in mutual:
        m += edit_count[couple[0]] * edit_count[couple[1]]
        if page == 'Gué_Pequeno':
            print(couple, edit_count[couple[0]] , edit_count[couple[1]] ,'=',edit_count[couple[0]] * edit_count[couple[1]])

    m *= len(mutual)

    if page == 'Gué_Pequeno':
        #print(mutual)
        print(edit_count['Phantomas'],edit_count['Dennis Radaelli'] )
        print(edit_count['DogoManagement'],edit_count['Causa83'] )
        print(edit_count['Jiassike'],edit_count['Dennis Radaelli'] )
    return m

def is_bot(user):
    words = re.compile('bot', re.IGNORECASE)
    
    if words.search(user): 
        return True 
    else: 
        return False
             


        
# %%
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))
pages_m = main()
ordinato = sorted(pages_m.items(), key=lambda k: k[1], reverse=True)[:20]
print(datetime.now() - inizio)

# %%
