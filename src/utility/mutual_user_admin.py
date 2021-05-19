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
count_mutual = {}
dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'

output = '/home/gandelli/dev/data/admin/user/mutual.tsv'



def mutual_monthly():
    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()

    # se in futuro non funzionerà è colpa di questo

    rev_id_dict = {}
    revertors = {} # revertors[username] = list of revid which reverted him
    editor = {} # editor[rev_id] = user who made the edit with id rev_id
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
            values = process_page(revertors, editor, current_page_id, edit_count, groups, page_name)

            #initialize new page
            revertors = {}
            editor = {}
            current_page_id = page_id
            current_page = page_name
            current_year_month = year_month
        
        else: 
            #current month finished
            if current_year_month != year_month:
                
                values = process_page(revertors, editor, current_page_id, edit_count, groups, page_name)
                current_year_month = year_month
        
   
        if is_reverted:
            if reverter_id not in rev_id_dict: # this prevents the multiple count of a revert 
                revertors.setdefault(username, []).append(reverter_id)
                rev_id_dict[reverter_id] = timestamp
    
        if is_reverter:
            editor[revision_id] = username




def analyze_mutuals_groups(mutual, group):
    global count_mutual
    for couple in mutual:
        #first user 
        if couple[0] not in count_mutual:
            count_mutual[couple[0]] = (0,0,0)

        (a, b, c) = count_mutual[couple[0]]
        livello = group[couple[1]]

        if livello == 'adm':
            a += 1
        elif livello == 'reg':
            b += 1
        elif livello == 'not':
            c += 1

        count_mutual[couple[0]] = (a, b, c)

        #second user 
        if couple[1] not in count_mutual:
            count_mutual[couple[1]] = (0,0,0)

        (a, b, c) = count_mutual[couple[1]]
        livello = group[couple[0]]

        if livello == 'adm':
            a += 1
        elif livello == 'reg':
            b += 1
        elif livello == 'not':
            c += 1

        count_mutual[couple[1]] = (a, b, c)
    


#return values about the number of mutual reverts that involves admin vs admin etc
def process_page(revertors, editor, page_id, edit_count, groups, page_name):

    
    reverted_m = utils.combine_editors(revertors, editor) # merge revertors and editor 
    mutual = utils.get_mutual(reverted_m, edit_count) # get a list of tuples  
    analyze_mutuals_groups(mutual, groups)# fill a dict with the info
    
def save():
    global count_mutual
    dump_out = open(output, 'w')
    dump_out.write('user\tgroup\tmutual_adm\tmutual_reg\tmutual_not\n') 

    for user, cose in count_mutual:
        print(user, cose)


    
# %%
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))
mutual_monthly()
print(datetime.now() - inizio)
# %%
