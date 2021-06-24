
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
import sys 

language = sys.argv[1]

contoedit = {}

dataset_tstamp = f'/home/gandelli/dev/data/dumps/{language}/sorted_by_timestamp.tsv.bz2'
output_monthly = f'/home/gandelli/dev/data/{language}/admin/user/reverts.tsv'


dump_out_monthly = open(output_monthly, 'w')

def users_rev():
    dump_in = bz2.open(dataset_tstamp, 'r')
    line = dump_in.readline()

   # se in futuro non funzionerà è colpa di questo
    dump_out_monthly.write('user\tgroup\tyear_month\ttot_received\tr_reg\tr_not\tr_adm\ttot_done\td_reg\td_not\td_adm\n') 
    

    rev_id_dict = {}
    revertors = {} # revertors[username] = list of revid which reverted him
    editor = {} # editor[rev_id] = user who made the edit with id rev_id
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
        year_month = str(timestamp.year)+'-'+timestamp.strftime('%m')




        #groups
        groups[username] = 'reg' if user_is_registered else 'not'
        if utils.is_admin(user_groups):
            groups[username] = 'adm'
        


        #current month finished
        if current_year_month != year_month:
            print(current_year_month )

            count_reverts(revertors, editor, groups, current_year_month)

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

    # for the last month
    count_reverts(revertors, editor, groups, current_year_month)

def count_reverts(revertors, editor, group, year_month):

    subiti = utils.combine_editors(revertors, editor)
    
   #get list of users a user reverted  
    fatti = {}
    for reverted, reverters in subiti.items():
        for reverter in reverters:
            fatti.setdefault(reverter, []).append(reverted)

    #count 
    for reverted, reverters in subiti.items():
        #subiti
        sreg = 0
        snot = 0
        sadm = 0
        
        for reverter in reverters:
            sreg += 1 if group[reverter] == 'reg' else 0
            snot += 1 if group[reverter] == 'not' else 0
            sadm += 1 if group[reverter] == 'adm' else 0

        #fatti
        freg = 0
        fnot = 0
        fadm = 0

        if reverted in fatti:
            for user in fatti[reverted]:
                if user in group:
                    freg += 1 if group[user] == 'reg' else 0
                    fnot += 1 if group[user] == 'not' else 0
                    fadm += 1 if group[user] == 'adm' else 0
        try:
            gruppo = group[reverted]
        except:
            gruppo = 'not'
            print('gruppo rotto per', reverted)
        
        # i do not want bots
        if not utils.is_bot(reverted):
            save_user_month(reverted, gruppo, year_month, sreg, snot, sadm, freg, fnot, fadm )

def save_user_month(user, group, month, sreg, snot, sadm, freg, fnot, fadm ):
    tot_subiti = sreg + snot + sadm
    tot_fatti = freg + fnot + fadm
    dump_out_monthly.write(f'{user}\t{group}\t{month}\t{tot_subiti}\t{sreg}\t{snot}\t{sadm}\t{tot_fatti}\t{freg}\t{fnot}\t{fadm}\n')



# %%
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))
users_rev()
print(datetime.now() - inizio)
# %%
