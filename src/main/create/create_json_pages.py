# %% create json contining info about chains 
import bz2
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
import os
import shutil
from utils import utils

dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'
output = '/home/gandelli/dev/data/wars_json/pages/'
output_no_anon = '/home/gandelli/dev/data/wars_json/pages_no_anon/'
#out_pages = '/home/gandelli/dev/data/pages.txt'

# l'ultima colonna è fals invece che false


# %% functions

#works
def simple_chains(anon = False):
    # dump_in = open(dataset, 'r')# for uncompressed
    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()

    #save_pages = open(out_pages, 'w')
    #pages_chains = open(out_pages_chains, 'w')
    
    i = 0
    #page
    chains = []
    n_reverts_in_chains = 0
    n_reverts = 0
    longest_chain = 0
    current_page_id = 0
    current_page = ''
    lunghezze = np.zeros(200)
    page_chains = {}
    stats = {}

    reverted_m = {} # all the users a user reverted 
    edit_count = {}
    pages_m = {}

    #chain
    chain = []
    users = {}
    start_date = ''
    end_date = ''
    reverter_id = 0
    reverted_user = ''
    
    while line != '':
       # line = dump_in.readline().rstrip()[:-1]# for uncompressed
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        # i want only namespace 0 and no vandalism
        if line == '' or values[28] != '0' or utils.is_vandalism(values[4]):
            continue
        if anon:
            if values[17] == 'true':
                continue

        
        #save fields from dataset
        page_name   = values[25]
        page_id     = int(values[23])

        rev_id      = values[52]
        reverter    = values[65]
        is_reverted = values[64]
        user        = values[6]
        user_edit_count = values[21]
        user_rev_count = values[21]
        timestamp = values[3]

        if user_edit_count != '':
            edit_count[user] = int(user_edit_count)
        else:
            edit_count[user] = 0

        n_reverts += 1

        #process new page
        if page_id != current_page_id:
             
            n_reverts_in_chains, longest_chain =  finish_chain(current_page, chain, users, start_date, end_date, lunghezze, n_reverts_in_chains, longest_chain, chains)

            #save past page
            if(len(chains) > 0): 
                g, involved = utils.getG(chains)
                m = utils.get_M(reverted_m, edit_count, current_page)
                savePage(current_page, chains, page_id, n_reverts_in_chains, longest_chain, g, list(lunghezze), m, n_reverts, anon)

                page_chains[current_page] = chains
                stats[current_page] = (n_reverts_in_chains/len(chains) , longest_chain, g)

            #initialize 
            #page
            current_page_id = page_id
            current_page = page_name
            chains = []
            n_reverts_in_chains = 0
            n_reverts = 0
            longest_chain = 0
            lunghezze = np.zeros(200)
            reverted_m = {}
            #chain
            chain = [rev_id]
            users = {}
            users[user] = user_rev_count
            start_date = values[3]
             
        else:
            #continue the chain
            if rev_id == reverter_id:                                   #if the currect reverts the previous one
                chain.append(rev_id)     
                users[user] = user_rev_count 
                end_date =  timestamp
                reverted_m.setdefault(user, []).append(reverted_user)     
                                  
            #finish the chain
            else:      
                
                n_reverts_in_chains, longest_chain = finish_chain(current_page, chain, users, start_date, end_date, lunghezze, n_reverts_in_chains, longest_chain, chains) 
                    
                #initialize
                chain = [rev_id]
                users = {}
                users[user] = user_rev_count
                start_date = timestamp
                

            if is_reverted == 'true':
                reverter_id = reverter # save
                reverted_user = user
    #pages_chains.write(list(page_chains))

    finish_files()
    return (page_chains, stats)



def finish_chain(page:str, chain:list , users: dict, start_date: str, end_date: str , lunghezze, n_reverts_in_chains: int, longest_chain: int,chains:list):

    if len(chain) > 2 and len(users) > 1 and not more_than_bot(users):
        chains.append({'page':page, 'revisions': chain, 'users' : users, 'len': len(chain), 'start': start_date, 'end': end_date})
        #compute page metrics
        lunghezze[len(chain)] +=1 # numbero of chains == n
        n_reverts_in_chains += len(chain)
        longest_chain = max(longest_chain, len(chain))
    return n_reverts_in_chains, longest_chain

#true if > 50% are bots
def more_than_bot(users):
 
    bot = 0
    utenti = 0
    for user in users:
        if utils.is_bot(user) :
             bot += 1
        else:
             utenti += 1
             
    if bot == 0:
        return False

    if utenti == 0:
        return True

    return utenti/bot > 1
            


def savePage(title, chains, id, n_reverts_in_chains, longest, g, lunghezze,m, n_reverts, anon):
    #print('salvo la pagina', title)


    n_files = 10
    if anon:
        path = f"{output_no_anon}wars_{ id % n_files}.json"
    else:
        path = f"{output}wars_{ id % n_files}.json"

    
    lun = {}
    dump_out = open(path, 'a')
    filesize = os.path.getsize(path)
    
    for i in range(1,len(lunghezze)):
        if(lunghezze[i] > 0):
            lun[i] = int(lunghezze[i])
    
    if filesize == 0:
        dump_out.write('[')

    mean = round(n_reverts_in_chains/len(chains), 1)
    
    dump_out.write(json.dumps({'title': title, 'chains': chains,'n_chains' : len(chains),'n_reverts_in_chains': n_reverts_in_chains,'n_reverts': n_reverts,'mean': mean,
                               'longest': longest, 'G' : g ,'M': m , 'lunghezze': lun})+',\n')
    dump_out.close()

def finish_files():
    for filename in os.listdir(output):
        print(filename)
        dump_out = open(output+filename, 'a')
        # andrebbe cancellata la virgola, uso questo trick per farlo sintatticamente corretto
        dump_out.write('{}]')

def get_DataFrame():

    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()
    df = []

    while line != '':

        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        df.append(values)

    return pd.DataFrame(df)


             


# %% SIMPLE with anon
shutil.rmtree(output) 
os.mkdir(output)
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))

s_chains, stats = simple_chains()
sorted(s_chains, key=lambda k: len(s_chains[k]), reverse=True)

lunga = sorted(stats.items(), key=lambda k: k[1][1], reverse=True)  # catena piu lunga
media = sorted(stats.items(), key=lambda k: k[1][0], reverse=True)  # media
numero = sorted(stats.items(), key=lambda k: k[1][2], reverse=True)  # media

print(datetime.now() - inizio)


#%%simple without anon
shutil.rmtree(output_no_anon) 
os.mkdir(output_no_anon)
inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))

s_chains, stats = simple_chains(True)
sorted(s_chains, key=lambda k: len(s_chains[k]), reverse=True)

lunga = sorted(stats.items(), key=lambda k: k[1][1], reverse=True)  # catena piu lunga
media = sorted(stats.items(), key=lambda k: k[1][0], reverse=True)  # media
numero = sorted(stats.items(), key=lambda k: k[1][2], reverse=True)  # media

print(datetime.now() - inizio)

# %% COMPLEX 
#inizio = datetime.now()
#c_chains = complex_chains()
#sorted(c_chains, key=lambda k: len(c_chains[k]), reverse=True)
#print(datetime.now() -inizio)



#%% sort pages by revert number

# df = get_DataFrame()
# df = df.filter([3, 4, 7, 25, 34, 64, 67], axis=1)
# df.columns = ['timestamp', 'commento', 'utente',
#               'pagina', 'edit_count', 'reverted', 'reverta']
# df_by_page = df.groupby(['pagina']).count().sort_values(
#     by=['utente'], ascending=False)


# %%
