# %% intro
import bz2
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
import os

import shutil


dataset = '/home/gandelli/dev/data/it/filtered_sorted_it.tsv.bz2'
#dataset = '/home/gandelli/dev/data/test/paradise.tsv'
output = '/home/gandelli/dev/data/wars/'
out_pages = '/home/gandelli/dev/data/pages.txt'
#out_pages_chains = '/home/gandelli/dev/data/pages_chains.txt'



# l'ultima colonna è fals invece che false


# %% functions

def complex_chains():

    #dump_in = bz2.open(dataset, 'r')
    dump_in = open(dataset, 'r')  # for uncompressed
    dump_out = open('wars.json', 'w')
    line = dump_in.readline()

    dump_out.write('[')

    inizio = datetime.now()

    open_chains = []
    complete_chains = []
    users = []
    page = ''
    page_chains = {}

    war = {
        "page": 'titolo',
        "chains": []

    }

    catena = {
        "users": ['pippo', 'pluto'],
        "revisions": []
    }

    while line != '':

        #line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        line = dump_in.readline().rstrip()[:-1]  # for uncompressed
        values = line.split('\t')

        if line == '' or len(values) < 69 or values[28] != '0':
            continue

        page_name = values[25]
        rev_id = values[52]
        reverter = values[65]
        is_reverted = values[64]
        utente = values[7]

        utenti = []

        added = False
        exist = False

        # check if this revision is part of a chain
        if page_name == page:
            for chain in open_chains:  # check if this rev is part of an existing  chain

                # if the one you want to insert already exists don't add it
                for i in range(len(chain)):
                    if chain[i] == reverter:
                        exist = True

                # if the last element of the chain match with the current revision id
                if chain[-1] == rev_id:
                    added = True
                    if is_reverted == 'true' and not exist:                           # continue the chain
                        chain.append(reverter)
                        utenti.append(utente)

                    else:                                               # end of the chain this revision is not reverted
                        if len(chain) > 2:
                            catena['revisions'] = chain
                            catena['users'] = utenti
                            war['chains'].append(catena)
                            complete_chains.append(chain)
                        open_chains.remove(chain)

            if not added and not exist:

                open_chains.append([rev_id, reverter])

        else:
            if(len(complete_chains) > 0):
                page_chains[page] = complete_chains
                war['page'] = page

                dump_out.write(json.dumps(war))
                dump_out.write(',\n')
            page = page_name
            complete_chains = []
            open_chains = []

    dump_out.write(']')
    return page_chains


def simple_chains():

    dump_in = bz2.open(dataset, 'r')
    # dump_in = open(dataset, 'r')# for uncompressed
    line = dump_in.readline()

    save_pages = open(out_pages, 'w')
    #pages_chains = open(out_pages_chains, 'w')
    
    i = 0

    chains = []
    chain = []
    
    page_chains = {}
    stats = {}
    users = {}
    total_reverts = 0
    longest_chain = 0
    reverter_id = 0
    current_page = ''
    lunghezze = np.zeros(200)

    while line != '':

        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        # line = dump_in.readline().rstrip()[:-1]# for uncompressed
        values = line.split('\t')

        # i want only namespace 0 and no vandalism
        if line == '' or values[28] != '0' or is_vandalism(values[4]):
            continue


    
        page_name   = values[25]
        rev_id      = values[52]
        reverter    = values[65]
        is_reverted = values[64]
        user        = values[7]
        page_id     = int(values[23])
        user_rev_count = values[21]

        #process new page
        if page_name != current_page:
            if len(chain) > 2 and len(users) > 1: 
                chains.append({'revisions':chain, 'users' : users,  'len': len(chain)})
                lunghezze[len(chain)] +=1

            #save past page
            if(len(chains) > 0): 
                m = getM(chains)
                savePage(current_page, chains, page_id, total_reverts, longest_chain, m, list(lunghezze))

                page_chains[current_page] = chains
                stats[current_page] = (total_reverts/len(chains) , longest_chain, m)

            #initialize 
            current_page = page_name
            chains = []
            total_reverts = 0
            longest_chain = 0
            lunghezze = np.zeros(200)

            chain = [rev_id]
            users = {}
            users[user] = user_rev_count
             
        else:
            #continue the chain
            if rev_id == reverter_id:                                   #if the currect reverts the previous one
                chain.append(rev_id)     
                users[user] = user_rev_count       
                                  
            #finish the chain
            else:      
                if len(chain) > 2 and len(users) > 1:
                    
                    chains.append({'revisions': chain, 'users' : users, 'len': len(chain)})
                    #compute page metrics
                    lunghezze[len(chain)] +=1 # numbero of chains == n
                    total_reverts += len(chain)
                    longest_chain = max(longest_chain, len(chain))
                
                #initialize
                chain = [rev_id]
                users = {}
                users[user] = user_rev_count
                

            if is_reverted == 'true':
                reverter_id = reverter # save
            
    #pages_chains.write(list(page_chains))

    finish_files()
    return (page_chains, stats)


def is_vandalism(comment):
    words = re.compile('vandal')
    if words.search(comment):
        return True
    else:
        return False


def savePage(title, chains, id, total_reverts, longest, m, lunghezze):
    #print('salvo la pagina', title)
    n_files = 10
    path = f"{output}wars_{ id % n_files}.json"
    lun = {}
    dump_out = open(path, 'a')
    filesize = os.path.getsize(path)
    
    for i in range(1,len(lunghezze)):
        if(lunghezze[i] > 0):
            lun[i] = lunghezze[i]
    
    if filesize == 0:
        dump_out.write('[')


    mean = round(total_reverts/len(chains), 1)
    
    dump_out.write(json.dumps({'title': title, 'chains': chains,'n_reverts': total_reverts,'mean': mean,
                               'longest': longest, 'M' : m , 'lunghezze': lun})+',\n')
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




# %% SIMPLE
shutil.rmtree(output) 
os.mkdir(output)
inizio = datetime.now()
s_chains, stats = simple_chains()
sorted(s_chains, key=lambda k: len(s_chains[k]), reverse=True)
lunga = sorted(stats.items(), key=lambda k: k[1][1], reverse=True)  # catena piu lunga
media = sorted(stats.items(), key=lambda k: k[1][0], reverse=True)  # media
numero = sorted(stats.items(), key=lambda k: k[1][2], reverse=True)  # media

print(datetime.now() - inizio)


# %% COMPLEX 
inizio = datetime.now()
c_chains = complex_chains()
sorted(c_chains, key=lambda k: len(c_chains[k]), reverse=True)
print(datetime.now() -inizio)



#%% sort pages by revert number

df = get_DataFrame()
df = df.filter([3, 4, 7, 25, 34, 64, 67], axis=1)
df.columns = ['timestamp', 'commento', 'utente',
              'pagina', 'edit_count', 'reverted', 'reverta']
df_by_page = df.groupby(['pagina']).count().sort_values(
    by=['utente'], ascending=False)


# %%

# %%


# %% non so perchè ma non funziona o  forse noon funziona l'altro


# %%
