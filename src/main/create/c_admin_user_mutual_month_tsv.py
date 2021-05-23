#%%
import bz2
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
import os
import shutil
from utils import utils

#%%

dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'

output = '/home/gandelli/dev/data/admin/user/mutuals.tsv'

dump_out = open(output, 'w')

def mutual_monthly():
    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()

    
    dump_out.write('user\tgroup\tpage_name\tyear_month\tmutual_with_admin\tmutual_with_reg\tmutual_with_not\n') 


    # se in futuro non funzionerà è colpa di questo

    rev_id_dict = {}
    revertors = {} # revertors[username] = list of revid which reverted him
    editor = {} # editor[rev_id] = user who made the edit with id rev_id
    count_admin = {}
    edit_count = {}
    groups = {}

    current_page_id = 0
    current_page = ''
    current_year_month = ''
    


    while line != '':
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        
        # i want only namespace 0 and no vandalism
        if line == '' or values[28] != '0' or utils.is_vandalism(values[4]):
            continue
        
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
        timestamp = datetime.strptime(values[3],'%Y-%m-%d %H:%M:%S.%f')
        year_month = str(timestamp.year)+'-'+str(timestamp.month)


        #edit count
        edit_count[username] = int(user_edit_count) if user_edit_count != '' else 0

        #groups
        groups[username] = 'reg' if user_is_registered else 'not'
        
        if utils.is_admin(user_groups):
            groups[username] = 'adm'
        
    
        #current page finished 
        if current_page_id != page_id:
            values = process_page(revertors, editor, current_page_id, edit_count, groups, page_name, current_year_month, count_admin)

            #initialize new page
            revertors = {}
            editor = {}
            count_admin = {}
            current_page_id = page_id
            current_page = page_name
            current_year_month = year_month
        
        else: 
            #current month finished
            if current_year_month != year_month:
                
                values = process_page(revertors, editor, current_page_id, edit_count, groups, page_name, current_year_month, count_admin)
                current_year_month = year_month
                count_admin = {}
                revertors = {}
                editor = {}
        
   
        if is_reverted:
            if reverter_id not in rev_id_dict: # this prevents the multiple count of a revert 
                revertors.setdefault(username, []).append(reverter_id)
                rev_id_dict[reverter_id] = timestamp
    
        if is_reverter:
            editor[revision_id] = username


def analyze_mutuals_groups(mutual, group,  year_month, page_name, count_admin):
 
    for couple in mutual:
        #first user 
        if couple[0] not in count_admin:
            count_admin[couple[0]] = (0,0,0)

        (a, b, c) = count_admin[couple[0]]
        livello = group[couple[1]]

        if livello == 'adm':
            a += 1
        elif livello == 'reg':
            b += 1
        elif livello == 'not':
            c += 1

        count_admin[couple[0]] = (a, b, c)

        #second user 
        if couple[1] not in count_admin:
            count_admin[couple[1]] = (0,0,0)

        (a, b, c) = count_admin[couple[1]]
        livello = group[couple[0]]

        if livello == 'adm':
            a += 1
        elif livello == 'reg':
            b += 1
        elif livello == 'not':
            c += 1

        count_admin[couple[1]] = (a, b, c)

        for user, values in count_admin.items():
            save(user, group[user], page_name, year_month, values[0], values[1], values[2])
    
        
#return values about the number of mutual reverts that involves admin vs admin etc
def process_page(revertors, editor, page_id, edit_count, groups, page_name, year_month, count_admin):


    reverted_m = utils.combine_editors(revertors, editor) # merge revertors and editor 
    mutual = utils.get_mutual(reverted_m, edit_count) # get a list of tuples  
    analyze_mutuals_groups(mutual, groups, year_month, page_name, count_admin)# fill a dict with the info


def save(user, group, page_name, year_month,adm, reg, not_reg):
    dump_out.write(f'{user}\t{group}\t{page_name}\t{year_month}\t{adm}\t{reg}\t{not_reg}\n')



    
# %%
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))
mutual_monthly()
print(datetime.now() - inizio)