# %% create json contining info about chains 
import bz2
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
import os

import shutil


dataset = '/home/gandelli/dev/data/it/sorted_by_pages.tsv.bz2'
output = '/home/gandelli/dev/data/wars_json/pages/'
#out_pages = '/home/gandelli/dev/data/pages.txt'

# l'ultima colonna è fals invece che false


# %% functions

#works
def simple_chains():
    # dump_in = open(dataset, 'r')# for uncompressed
    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()

    #save_pages = open(out_pages, 'w')
    #pages_chains = open(out_pages_chains, 'w')
    
    i = 0
    #page
    chains = []
    total_reverts = 0
    longest_chain = 0
    current_page_id = 0
    current_page = ''
    lunghezze = np.zeros(200)
    page_chains = {}
    stats = {}

    #chain
    chain = []
    users = {}
    start_date = ''
    end_date = ''
    reverter_id = 0
    
    while line != '':
       # line = dump_in.readline().rstrip()[:-1]# for uncompressed
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        # i want only namespace 0 and no vandalism
        if line == '' or values[28] != '0' or is_vandalism(values[4]):
            continue


        #save fields from dataset
        page_name   = values[25]
        rev_id      = values[52]
        reverter    = values[65]
        is_reverted = values[64]
        user        = values[6]
        page_id     = int(values[23])
        user_rev_count = values[21]
        timestamp = values[3]

        #process new page
        if page_id != current_page_id:
             
            total_reverts, longest_chain =  finish_chain(current_page, chain, users, start_date, end_date, lunghezze, total_reverts, longest_chain, chains)

            #save past page
            if(len(chains) > 0): 
                g = getG(chains)
                savePage(current_page, chains, page_id, total_reverts, longest_chain, g, list(lunghezze))

                page_chains[current_page] = chains
                stats[current_page] = (total_reverts/len(chains) , longest_chain, g)

            #initialize 
            #page
            current_page_id = page_id
            current_page = page_name
            chains = []
            total_reverts = 0
            longest_chain = 0
            lunghezze = np.zeros(200)
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
                                  
            #finish the chain
            else:      
                
                total_reverts, longest_chain = finish_chain(current_page, chain, users, start_date, end_date, lunghezze, total_reverts, longest_chain, chains)
                    
                #initialize
                chain = [rev_id]
                users = {}
                users[user] = user_rev_count
                start_date = timestamp
                

            if is_reverted == 'true':
                reverter_id = reverter # save
            
    #pages_chains.write(list(page_chains))

    finish_files()
    return (page_chains, stats)

def finish_chain(page, chain, users, start_date, end_date, lunghezze, total_reverts, longest_chain,chains):

    if len(chain) > 2 and len(users) > 1 and not isBot(users):
        chains.append({'page':page, 'revisions': chain, 'users' : users, 'len': len(chain), 'start': start_date, 'end': end_date})
        #compute page metrics
        lunghezze[len(chain)] +=1 # numbero of chains == n
        total_reverts += len(chain)
        longest_chain = max(longest_chain, len(chain))
    return total_reverts, longest_chain
#true if > 50% are bots
def isBot(users):
   
    words = re.compile('bot', re.IGNORECASE)
    bot = 0
    utenti = 0
    for user in users:
        if words.search(user) :
             bot += 1
        else:
             utenti += 1
    if bot == 0:
        return False

    if  utenti/bot > 1:
        return False
    else:
        return True
            
def is_vandalism(comment ):
    words = re.compile('vandal')
    if words.search(comment) :
        return True
    else:
        return False

def savePage(title, chains, id, total_reverts, longest, g, lunghezze):
    #print('salvo la pagina', title)
    n_files = 10
    path = f"{output}wars_{ id % n_files}.json"
    lun = {}
    dump_out = open(path, 'a')
    filesize = os.path.getsize(path)
    
    for i in range(1,len(lunghezze)):
        if(lunghezze[i] > 0):
            lun[i] = int(lunghezze[i])
    
    if filesize == 0:
        dump_out.write('[')


    mean = round(total_reverts/len(chains), 1)
    
    dump_out.write(json.dumps({'title': title, 'chains': chains,'n_chains' : len(chains),'n_reverts': total_reverts,'mean': mean,
                               'longest': longest, 'G' : g , 'lunghezze': lun})+',\n')
    dump_out.close()

def finish_files():
    for filename in os.listdir(output):
        print(filename)
        dump_out = open(output+filename, 'a')
        # andrebbe cancellata la virgola, uso questo trick per farlo sintatticamente corretto
        dump_out.write('{}]')

def getG(chains):
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

def get_DataFrame():

    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()
    df = []

    while line != '':

        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        df.append(values)

    return pd.DataFrame(df)




# %% SIMPLE
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
