#%% 10 min  info about reverts made in a page (adm, reg)
import bz2
import subprocess
import os
from datetime import datetime
from utils import utils
import re


dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'
output = '/home/gandelli/dev/data/admin/page/reverts.tsv'


dump_out = open(output, 'w')

def reverts():
    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()

   
    dump_out.write('page_id\tpage_name\tyear_month\tadm_adm\tadm_reg\treg_adm\treg_reg\tnot_reg\treg\n')

    reverted_user = ''
    reverted_is_admin = False
    reverted_is_registered = False
    reverter_id = 0
    current_page_id = 0
    current_page = ''
    current_year_month = ''

    n_adm_adm = 0
    n_adm_reg = 0
    n_reg_adm = 0
    n_reg_reg = 0

    n_not_reg = 0



    while line != '':
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        #filter namespace != 0 vandalsm and not revision and no bot
        if line == '' or values[28] != '0' or utils.is_vandalism(values[4]) or len(values) < 2 or values[1] != 'revision'or utils.is_bot(values[6]):
                continue


        #parse from dataset
        page_id = int(values[23])
        page_name = values[25]
        user = values[6]
        user_edit_count = values[21]
        user_is_registered = not utils.to_bool(values[17])
        user_groups = values[11]
        rev_id = values[52]
        reverter = values[65]
        is_reverted = utils.to_bool((values[64]))
        timestamp = datetime.strptime(values[3],'%Y-%m-%d %H:%M:%S.%f')
        #year_month = str(timestamp.year)+'-'+str(timestamp.month)
        year_month = str(timestamp.year)+'-'+timestamp.strftime('%m')


        
        # current page is finished 
        if page_id != current_page_id:
            process_page(current_page, n_adm_adm, n_adm_reg, n_reg_adm, n_reg_reg , n_not_reg ,current_page_id, current_year_month)

            #initialize new page 
            current_page_id = page_id
            current_page = page_name
            current_year_month = year_month
            n_adm_adm = 0
            n_adm_reg = 0
            n_reg_adm = 0
            n_reg_reg = 0
            n_not_reg = 0
        else:
            #current month finished 
            if current_year_month != year_month:

                process_page(current_page, n_adm_adm, n_adm_reg, n_reg_adm, n_reg_reg , n_not_reg ,current_page_id, current_year_month)

                current_year_month = year_month

        
        if reverter_id == rev_id:
    
            if user != reverted_user:

                #at least one anon 
                if not user_is_registered or not reverted_is_registered:
                    n_not_reg += 1
                

                #admin vs admin
                if utils.is_admin(user_groups) and reverted_is_admin:
                    n_adm_adm += 1
                    
                # normal vs normal
                if user_is_registered and not utils.is_admin(user_groups) and reverted_is_registered and not reverted_is_admin:
                    n_reg_reg += 1
                    
                # admin vs normal
                if utils.is_admin(user_groups) and reverted_is_registered and not reverted_is_admin:
                    n_adm_reg += 1
                    
                #normal vs admin
                if user_is_registered and not utils.is_admin(user_groups) and reverted_is_admin:
                    n_reg_adm += 1
                

        if is_reverted:
            reverter_id = reverter

            reverted_is_admin = utils.is_admin(user_groups)
            reverted_is_registered = user_is_registered
            reverted_user = user
        

    dump_in.close()

def process_page(page_name, adm_adm, adm_reg, reg_adm, reg_reg , not_reg, page_id, year_month ):
    reg = adm_adm+ adm_reg+ reg_adm+ reg_reg
    if page_name != r'\"':
        dump_out.write(f'{page_id}\t{page_name}\t{year_month}\t{adm_adm}\t{adm_reg}\t{reg_adm}\t{reg_reg}\t{not_reg}\t{reg}\n')





# %%
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))
reverts()
print(datetime.now() - inizio)
# %%
