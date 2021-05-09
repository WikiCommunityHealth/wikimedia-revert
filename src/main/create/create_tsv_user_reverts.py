
#%% create a tsv file from the filtered dataset with metrics about mutual reverts (admin, reg)
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

output_monthly = '/home/gandelli/dev/data/monthly/pages/mutual.tsv'

dump_out_monthly = open(output_monthly, 'w')

def users_rev():
    dump_in = bz2.open(dataset_tstamp, 'r')
    line = dump_in.readline()

    rev_id_dict = {}
    revertors = {} # revertors[username] = list of revid which reverted him
    editor = {} # editor[rev_id] = user who made the edit with id rev_id
    edit_count = {}
    groups = {}
    current_page_id = 0
    current_page = ''
    current_year_month = ''
    
    # se in futuro non funzionerà è colpa di questo
    dump_out_monthly.write('page_id\tpage_name\tyear_month\tadm_adm\tadm_reg\treg_reg\tnot_reg\treg\n') 


    while line != '':
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        
        # i want only namespace 0 and no vandalism
        if line == '' or values[28] != '0':
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
        


        #current month finished
        if current_year_month != year_month:
            print(current_year_month )
            print(utils.combine_editors(revertors, editor) , '\n')
            print(groups, '\n\n')

            count_reverts(revertors, editor, groups)

            revertors = {}
            editor = {}
            groups = {}
            current_year_month = year_month
        
   
        if is_reverted:
            if reverter_id not in rev_id_dict: # this prevents the multiple count of a revert 
                revertors.setdefault(username, []).append(reverter_id)
                rev_id_dict[reverter_id] = timestamp
    
        if is_reverter:
            editor[revision_id] = username


# %%

def count_reverts(revertors, editor, groups):
    subiti = utils.combine_editors(revertors, editor)


# %%
def test(comb, month, group):
    
    for uomo, reverters in comb.items():
        sreg = 0
        snot = 0
        sadm = 0
        for reverter in reverters:
            sreg += 1 if group[reverter] == 'reg' else 0
            snot += 1 if group[reverter] == 'not' else 0
            sadm += 1 if group[reverter] == 'adm' else 0
                

        print(uomo, group[uomo], month, sreg, snot, sadm)
# %%
comb = {'Danilo': ['Frieda'], '81.250.141.227': ['Frieda', 'Frieda'], 'Frieda': ['81.250.141.227'], 'Gianluigi': ['Frieda'], 'Rafaele liraz': ['Frieda'], '212.162.77.106': ['Frieda'], '194.244.68.198': ['MikyT'], '200.53.106.46': ['Alfio'], 'Alfio': ['Ayeye'], '219.150.156.3': ['Suisui'], 'Snowdog': ['Thkperson'], 'Thkperson': ['Snowdog'], '167.83.10.23': ['Frieda', 'Frieda'], '213.45.38.11': ['Svante']} 
group = {'Twice25': 'reg', '82.84.228.70': 'not', 'Danilo': 'reg', 'Frieda': 'adm', '81.250.141.227': 'not', 'Gianluigi': 'reg', 'Rafaele liraz': 'reg', 'Renato Caniatti': 'reg', '82.84.57.181': 'not', 'Kurdt': 'reg', 'Ayeye': 'reg', '212.162.77.106': 'not', '194.244.68.198': 'not', 'MikyT': 'reg', '200.53.106.46': 'not', 'Alfio': 'reg', 'Spino': 'reg', '219.150.156.3': 'not', 'Thkperson': 'reg', 'Suisui': 'reg', 'Snowdog': 'reg', '213.23.133.224': 'not', 'Pérvasion': 'reg', '167.83.10.23': 'not', '213.45.38.11': 'not', 'Svante': 'reg', '81.116.244.202': 'not', '219.104.1.239': 'not', '151.35.68.116': 'not'}
# %%
