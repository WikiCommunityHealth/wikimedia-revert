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
# %%

page_monthly()
#%%

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
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))
pages_m = main()
ordinato = sorted(pages_m.items(), key=lambda k: k[1], reverse=True)[:20]
print(datetime.now() - inizio)

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


# %%

#bisogna levare i bot 
#alcuni simboli non conta tutti gli edit 
def page_monthly():
    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()

    
    revertors = {} # revertors[username] = list of revid which reverted him
    editor = {} # editor[rev_id] = user who made the edit with id rev_id
    edit_count = {}

    current_page_id = 0

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
        is_reverted = values[64]
        is_reverter = values[67]
        reverter_id = values[65]
        page_id = values[23]
        page_name = values[24]
        user_edit_count = values[21]

        if page_id == '2829':
            print(values[23], 'e ', values[24])
            print(values[24], values[52])

        #edit count
        if user_edit_count != '':
            edit_count[username] = int(user_edit_count)
        else:
            edit_count[username] = 0
        
    
        #current page finished 
        if current_page_id != page_id:
            process_page(revertors, editor, current_page_id, edit_count)

            revertors = {}
            editor = {}
            current_page_id = page_id
        

        if is_reverted == 'true':
            revertors.setdefault(username, []).append(reverter_id)
    
        if is_reverter == 'true':
            editor[revision_id] = username




    

def process_page(revertors, editor, page_id, edit_count):
    print('processo page'+str(page_id))
    print(revertors)
    print(editor)

    reverted_m = {}

    for user, reverters in revertors.items():
        for reverter in reverters:
            reverted_m.setdefault(user, []).append(editor[reverter])
    
    #m = utils.get_M(reverted_m, edit_count, page_id)
    #print(m)
    #return m


# %%
rev = {'85.20.122.240': ['1725921'], 
'84.163.75.174': ['5038831'], 
'87.139.125.203': ['5319592'], 
'84.227.188.19': ['7450483'], 
'82.53.146.4': ['16596678'], 
'83.225.245.75': ['18787901'], 
'87.25.172.60': ['21099895'], 
'79.39.123.36': ['22142782', '22142923'], '79.22.32.108': ['25393435', '25393435'], '82.57.149.34': ['27004467'], '93.146.198.6': ['29431708'], '81.74.114.109': ['29991424', '29991424'], '79.51.244.104': ['30139169'], '79.51.243.35': ['30139169'], '151.64.34.233': ['30585002'], '77.240.231.182': ['30915646'], 'Xqbot': ['31190955'], 'ArthurBot': ['31377653'], '84.227.113.192': ['35319405', '35319437'], '79.51.9.70': ['37304914'], '62.210.154.242': ['37322775'], '151.64.90.72': ['38793586', '38793586'], '79.47.31.54': ['44925977'], '77.29.112.22': ['46100929', '46100929'], '79.10.235.130': ['48516081', '48516136'], '93.38.170.184': ['50176195'], '151.51.190.206': ['54133754'], '188.218.214.160': ['58730798'], '93.46.196.188': ['63718677'], 'Bruna dalla vecchia': ['67501889'], '80.117.222.124': ['69530575'], '88.46.239.43': ['70785438', '71011603'], '5.170.198.233': ['79368116', '79368236', '79368272', '79368352', '79368383', '79368403', '79368448', '79368574', '79368611', '79368789'], 'Bellatrovata': ['79368217', '79368249', '79368333', '79368360', '79368390', '79368417', '79368536', '79368585', '79368771', '79368855'], '93.34.234.148': ['79368962']}
editor = {'1725921': 'Civvi', '5038831': 'Rojelio', '5319592': 'Dario vet', '7450483': 'Brownout', '16596678': 'DarkAp89~itwiki', '18787901': 'Manutius', '21099895': 'Melos', '22142782': 'Tia solzago', '22142923': 'Sbazzone', '25393435': '.mau.', '27004467': '151.20.234.243', '29431708': 'Gac', '29991424': '213.149.223.21', '30139169': '.mau.', '30585002': '.mau.', '30915646': 'Guidomac', '31190955': 'HRoestBot', '31377653': 'Xqbot', '35319405': 'Taueres', '35319437': 'Taueres', '37304914': 'Sbisolo', '37322775': 'YukioSanjo', '38793586': 'L736E', '44925977': 'Frigotoni', '46100929': 'Ignlig', '48516081': 'Petrik Schleck', '48516136': 'Vituzzu', '50176195': 'Dega180', '54133754': 'Johnlong', '58730798': 'Madaki', '63718677': 'Bradipo Lento', '67501889': 'Ary29', '69530575': '80.117.222.124', '70785438': 'Phantomas', '71011603': 'Phantomas', '79368116': 'Bellatrovata', '79368217': '5.170.198.233', '79368236': 'Bellatrovata', '79368249': '5.170.198.233', '79368272': 'Bellatrovata', '79368333': '5.170.198.233', '79368352': 'Bellatrovata', '79368360': '5.170.198.233', '79368383': 'Bellatrovata', '79368390': '5.170.198.233', '79368403': 'Bellatrovata', '79368417': '5.170.198.233', '79368448': 'Bellatrovata', '79368536': '5.170.198.233', '79368574': 'Bellatrovata', '79368585': '5.170.198.233', '79368611': 'Bellatrovata', '79368771': '5.170.198.233', '79368789': 'Bellatrovata', '79368855': '5.170.196.16', '79368962': 'Bellatrovata', '79373845': 'Pequod76'}

fine = {'85.20.122.240': ['Civvi'], '84.163.75.174': ['Rojelio'], '87.139.125.203': ['Dario vet'], '84.227.188.19': ['Brownout'], '82.53.146.4': ['DarkAp89~itwiki'], '83.225.245.75': ['Manutius'], '87.25.172.60': ['Melos'], '79.39.123.36': ['Tia solzago', 'Sbazzone'], '79.22.32.108': ['.mau.', '.mau.'], '82.57.149.34': ['151.20.234.243'], '93.146.198.6': ['Gac'], '81.74.114.109': ['213.149.223.21', '213.149.223.21'], '79.51.244.104': ['.mau.'], '79.51.243.35': ['.mau.'], '151.64.34.233': ['.mau.'], '77.240.231.182': ['Guidomac'], 'Xqbot': ['HRoestBot'], 'ArthurBot': ['Xqbot'], '84.227.113.192': ['Taueres', 'Taueres'], '79.51.9.70': ['Sbisolo'], '62.210.154.242': ['YukioSanjo'], '151.64.90.72': ['L736E', 'L736E'], '79.47.31.54': ['Frigotoni'], '77.29.112.22': ['Ignlig', 'Ignlig'], '79.10.235.130': ['Petrik Schleck', 'Vituzzu'], '93.38.170.184': ['Dega180'], '151.51.190.206': ['Johnlong'], '188.218.214.160': ['Madaki'], '93.46.196.188': ['Bradipo Lento'], 'Bruna dalla vecchia': ['Ary29'], '80.117.222.124': ['80.117.222.124'], '88.46.239.43': ['Phantomas', 'Phantomas'], '5.170.198.233': ['Bellatrovata', 'Bellatrovata', 'Bellatrovata', 'Bellatrovata', 'Bellatrovata', 'Bellatrovata', 'Bellatrovata', 'Bellatrovata', 'Bellatrovata', 'Bellatrovata'], 'Bellatrovata': ['5.170.198.233', '5.170.198.233', '5.170.198.233', '5.170.198.233', '5.170.198.233', '5.170.198.233', '5.170.198.233', '5.170.198.233', '5.170.198.233', '5.170.196.16'], '93.34.234.148': ['Bellatrovata']}
# %%
