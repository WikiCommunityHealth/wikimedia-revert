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
dataset_tstamp = '/home/gandelli/dev/data/it/sorted_by_timestamp.tsv.bz2'

output = '/home/gandelli/dev/data/pages_data/mutual_reverts_admin.tsv'

dump_out = open(output, 'w')
dump_out.write('page_id\tpage_name\tadm_adm\tadm_reg\treg_reg\tnot_reg\treg\n')


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
                print('aggiungo')
            if is_reverted == 'true':
                reverter_id = reverter
                reverted_user = user
    return pages_m

# pass every time the edit count so it consider the edit count at the time of the revert


  
# %%
# inizio = datetime.now()
# print(inizio.strftime(" %H:%M:%S"))
# pages_m = main()
# ordinato = sorted(pages_m.items(), key=lambda k: k[1], reverse=True)[:20]
# print(datetime.now() - inizio)

# %%
month_m = {}
def monthly():
    dump_in = bz2.open(dataset_tstamp, 'r')
    line = dump_in.readline()


     # all the users a user reverted 
    current_year_month  = ''
    reverter_id = 0
    reverted_user = ''
    edit_count = {}
    reverted_m = {}

    while line != '':
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

    # i want only namespace 0 and no vandalism
        if line == '' or values[28] != '0':
            continue

        #parse ftom dataset
        timestamp = datetime.strptime(values[3],'%Y-%m-%d %H:%M:%S.%f')
        user = values[6]
        rev_id = values[52]
        user_edit_count = values[21]

        #edit count
        if user_edit_count != '':
            edit_count[user] = int(user_edit_count)
        else:
            edit_count[user] = 0


        year_month = str(timestamp.year)+'-'+str(timestamp.month)

        #finish of the month 
        if current_year_month != year_month:

            month_m[year_month] = utils.get_M(reverted_m, edit_count, 'page')
            print(year_month)
            print(reverted_m)
            
            current_year_month = year_month
            reverted_m = {}
        else: #continue the month
            if rev_id == reverter_id: ##if the currect reverts the previous one
                reverted_m.setdefault(user, []).append(reverted_user)
            else:
                reverter_id = rev_id
                reverted_user = user


#%%
def boh():
    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()

    rev_id_dict = {}
    revertors = {} # revertors[username] = list of revid which reverted him
    editor = {} # editor[rev_id] = user who made the edit with id rev_id
    edit_count = {}
    groups = {}
    current_page_id = 0
    current_page = ''
    

    while line != '':
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        
        # i want only namespace 0 and no vandalism
        if line == '' or values[28] != '0':
            continue
        #print(line)
        
        #parse from dataset
        revision_id = values[52]
        username = values[6]
        timestamp = values[3]
        is_reverted = utils.to_bool(values[64])
        is_reverter = utils.to_bool(values[67])
        reverter_id = values[65]
        page_id = values[23]
        page_name = values[24]
        user_edit_count = values[21]
        user_is_registered = not utils.to_bool(values[17])
        user_groups = values[11]


        #current page finished 
        if current_page_id != page_id:

            pass


        if is_reverted:
            if reverter_id not in rev_id_dict:
                revertors.setdefault(username, []).append(reverter_id)
                rev_id_dict[reverter_id] = timestamp
    
        if is_reverter:
            editor[revision_id] = username


