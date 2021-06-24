#%% 20 min create a tsv file from the filtered dataset with metrics about mutual reverts (admin, reg)
import bz2
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
import os
from utils import utils
import shutil
import sys 

language = sys.argv[1]

contoedit = {}
dataset = f'/home/gandelli/dev/data/dumps/{language}/sorted_by_pages.tsv.bz2'
dataset_tstamp = f'/home/gandelli/dev/data/dumps/{language}/sorted_by_timestamp.tsv.bz2'

output_monthly = f'/home/gandelli/dev/data/{language}/admin/page/mutuals.tsv'

dump_out_monthly = open(output_monthly, 'w')



#%% functions

def mutual_monthly():
    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()

    # se in futuro non funzionerà è colpa di questo
    dump_out_monthly.write('page_id\tpage_name\tyear_month\tM\tmut_adm_adm\tmut_adm_reg\tmut_reg_reg\tmut_not_reg\tmut_reg\n') 

    rev_id_dict = {}
    revertors = {} # revertors[username] = list of revid which reverted him
    editor = {} # editor[rev_id] = user who made the edit with id rev_id
    edit_count  = {}
    groups = {}
    involved = set()


    current_page_id = 0
    current_page = ''
    current_year_month = ''


    


    while line != '':
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        
        # i want only namespace 0 and no vandalism
        if line == '' or values[28] != '0' or utils.is_vandalism(values[4]) or utils.is_bot(values[6]):
            continue
        
        #parse from dataset
        revision_id = values[52]
        username = values[6]
        timestamp = values[3]
        is_reverted = utils.to_bool(values[64])
        is_reverter = utils.to_bool(values[67])
        reverter_id = values[65]
        page_id = values[23]
        page_name = values[25]
        user_edit_count = values[21]
        user_is_registered = not utils.to_bool(values[17])
        user_groups = values[11]
        timestamp = datetime.strptime(values[3],'%Y-%m-%d %H:%M:%S.%f')
        year_month = str(timestamp.year)+'-'+timestamp.strftime('%m')

        #involved
        involved.add(username)
        #edit count
        edit_count[username] = int(user_edit_count) if user_edit_count != '' else 0

        #groups
        groups[username] = 'reg' if user_is_registered else 'not'
        
        if utils.is_admin(user_groups):
            groups[username] = 'adm'
        
    
        #current page finished 
        if current_page_id != page_id:
            values = process_page(revertors, editor, current_page_id, edit_count, groups, current_page, involved)
            save_page_month(current_page,  current_page_id,values, current_year_month)

            #initialize new page
            revertors = {}
            editor = {}
            involved = set()
            current_page_id = page_id
            current_page = page_name
            current_year_month = year_month
        
        else: 
            #current month finished
            if current_year_month != year_month:
                
                values = process_page(revertors, editor, current_page_id, edit_count, groups, current_page, involved)
                save_page_month(current_page,  current_page_id,values, current_year_month)
                current_year_month = year_month
        
   
        if is_reverted:
            if reverter_id not in rev_id_dict: # this prevents the multiple count of a revert 
                revertors.setdefault(username, []).append(reverter_id)
                rev_id_dict[reverter_id] = timestamp
    
        if is_reverter:
            editor[revision_id] = username

#return values about the number of mutual reverts that involves admin vs admin etc
def process_page(revertors, editor, page_id, edit_count, groups, page_name, involved):
    
    reverted_m = utils.combine_editors(revertors, editor)

    mutual = utils.get_mutual(reverted_m, edit_count)
    m = utils.get_M(reverted_m, edit_count, len(involved))


    return analyze_mutuals_groups(page_id, page_name, mutual, groups, m)
    
def analyze_mutuals_groups(page_id, page_name, mutuals,groups, m):

    reg_reg = False
    not_reg = False
    adm_reg = False 
    adm_adm = False

    values = {}
    values['n_adm_adm'] = 0
    values['n_adm_reg'] = 0
    values['n_reg_reg'] = 0
    values['n_not_reg'] = 0
    values['M'] = m

    for couple in mutuals:
        first = groups[couple[0]] if couple[0] in groups else 'not'
        second = groups[couple[1]] if couple[1] in groups else 'not'
        
        
        reg_reg = (first == 'reg' and second == 'reg')
        not_reg = (first == 'not' or  second == 'not')
        adm_reg = (first == 'adm' and second == 'reg') or (first == 'reg' and second == 'adm')
        adm_adm = (first == 'adm' and second == 'adm')

        
        if not_reg:
            values['n_not_reg'] += 1
        
        if reg_reg:
            values['n_reg_reg'] += 1
        
        if adm_adm:
            values['n_adm_adm'] += 1
        
        if adm_reg:
            values['n_adm_reg'] += 1
    
    return values


def save_page_month(page_name, page_id ,values, year_month):
    adm_adm = values['n_adm_adm']
    adm_reg = values['n_adm_reg']
    reg_reg = values['n_reg_reg']
    not_reg = values['n_not_reg']
    M  = values['M']
    reg = adm_adm + adm_reg + reg_reg
    dump_out_monthly.write(f'{page_id}\t{page_name}\t{year_month}\t{M}\t{adm_adm}\t{adm_reg}\t{reg_reg}\t{not_reg}\t{reg}\n')



# %% mutual per mese 
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))

mutual_monthly()

print(datetime.now() - inizio)
# %%

# %%
