
#%%
# PAGE EXAMPLE
# {'title': 'Zuppa_di_pesce_(film)',
#  'chains': [{'revisions': ['95861493', '95861612', '95973728'],
#    'users': {'93.44.99.33': '', 'Kirk39': '63558', 'AttoBot': '482488'},
#    'len': 3,
#    'start': '2018-04-01 04:54:40.0',
#    'end': '2018-04-05 07:36:26.0'}],
#  'n_chains': 1,
#  'n_reverts': 3,
#  'mean': 3.0,
#  'longest': 3,
#  'M': 0,
#  'lunghezze': {'3': 1}}

import json
from datetime import datetime
import numpy as np
import pandas as pd
import os
import shutil


dataset_folder = '/home/gandelli/dev/data/wars_json/pages/'
output = '/home/gandelli/dev/data/wars_json/users/'



#%%
def get_users():
    users = {}

    i = 10 # number of files in the wars folder
    for i in range (0,i):
        dump_in = open(f"{dataset_folder}wars_{i}.json")
        line = dump_in.readline()
        while(line != ''):
            line = dump_in.readline()
            if line == '{}]' or line == '':
                continue
            page = json.loads(line[:-2])
            for chain in page['chains']:
                for user in chain['users']:
                    users.setdefault(user, []).append(chain)
    
    return users

def compute_users(users):
    i = 0
    for user,chains in users.items():
        name = user
        total_reverts = 0
        longest = 0
        lunghezze = np.zeros(200)

        m = getM(chains)
        for chain in chains:
            total_reverts += chain['len']
            longest = max(longest, chain['len'])
            lunghezze[chain['len']] +=1
        
        save_user(name, chains, total_reverts, longest, m, lunghezze, i)
        i+=1
    
    finish_files()
        
def save_user(name, chains, total_reverts, longest, m, lunghezze, n):
    mean = round(total_reverts/len(chains), 1)
    lun = {}
    n_files = 10
    path = f"{output}wars_{ n % n_files}.json"
    dump_out = open(path, 'a')
    filesize = os.path.getsize(path)

    for i in range(1,len(lunghezze)):
        if(lunghezze[i] > 0):
            lun[i] = int(lunghezze[i])

    if filesize == 0:
        dump_out.write('[')

    dump_out.write(json.dumps({'user': name, 'chains': chains,'n_chains' : len(chains),'n_reverts': total_reverts,'mean': mean, 'longest': longest, 'M' : m , 'lunghezze': lun})+',\n')

def getM(chains):
    tot = 0
    utenti = set()
    for chain in chains:
        a = 9999999999
    
        for user in chain['users']:
            utenti.add(user)
            if chain['users'][user] != '':
                a =  min(a, int(chain['users'][user])) # for every chain in a page i take the users involved and i extract the minimun revision count
            else:
                a = min(a, 0)
        tot += a

    return (tot * len(utenti))  

def finish_files():
    for filename in os.listdir(output):
        print(filename)
        dump_out = open(output+filename, 'a')
        # andrebbe cancellata la virgola, uso questo trick per farlo sintatticamente corretto
        dump_out.write('{}]')

#%%
shutil.rmtree(output) 
os.mkdir(output)
users = get_users()
compute_users(users)



# %%

