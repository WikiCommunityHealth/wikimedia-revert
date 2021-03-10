# %% intro
import bz2
import pandas as pd
from datetime import datetime
import json
import re
import os

dataset = '/home/gandelli/dev/data/it/filtered_sorted_it.tsv.bz2'
#dataset = '/home/gandelli/dev/data/test/toscana_sorted.tsv'
output = '/home/gandelli/dev/data/wars/'


#l'ultima colonna è fals invece che false 



#%% functions 

def complex_chains():
    

    #dump_in = bz2.open(dataset, 'r') 
    dump_in = open(dataset, 'r')# for uncompressed 
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
        line = dump_in.readline().rstrip()[:-1]# for uncompressed 
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

        #check if this revision is part of a chain
        if page_name == page:
            for chain in open_chains:                                   #check if this rev is part of an existing  chain

                for i in range(len(chain)):                             # if the one you want to insert already exists don't add it 
                    if chain[i] == reverter:
                        exist = True

                if chain[-1] == rev_id:                                 # if the last element of the chain match with the current revision id
                    added = True
                    if is_reverted == 'true' and not exist:                           # continue the chain
                        chain.append(reverter)
                        utenti.append(utente)
                         
                    else:                                               # end of the chain this revision is not reverted 
                        if len(chain) > 2 :
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
    #dump_in = open(dataset, 'r')# for uncompressed 
    line = dump_in.readline()
    
    i = 0

    reverter_id = 0
    chains = []
    chain = []
    current_page = ''
    page_chains = {}
    stats = {}
    users = set()
    total_reverts = 0
    longest_chain = 0
    
    while line != '':

        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        #line = dump_in.readline().rstrip()[:-1]# for uncompressed 
        values = line.split('\t')

        if line == '' or values[28] != '0' or is_vandalism(values[4]): # i want only namespace 0 and no vandalism
            continue

        
        
        page_name   = values[25]
        rev_id      = values[52]
        reverter    = values[65]
        is_reverted = values[64]
        user        = values[7]
        page_id     = int(values[23])

        if page_name != current_page:                       #process new page 
            
            if(len(chains) > 0):
                savePage(current_page, chains, page_id, total_reverts/len(chains), longest_chain)
                page_chains[current_page] = chains
                stats[current_page] = (total_reverts/len(chains) , longest_chain)
                #print(current_page, total_reverts/len(chains), longest_chain)
                i+=1

            current_page = page_name    
            chains = [] 
            total_reverts = 0
            longest_chain = 0
             
        else:
            if rev_id == reverter_id:                                   #if the currect reverts the previous one
                chain.append(rev_id)     
                users.add(user)                               # continue the chain
            else:
                if len(chain) > 2:
                    chains.append({'revisions':chain, 'users' : list(users)})
                    total_reverts += len(chain)
                    longest_chain = max(longest_chain, len(chain))
                chain = [rev_id]
                users = {user}
                

            if is_reverted == 'true':
                reverter_id = reverter # save
            
    finish_files()
    return (page_chains,stats)

def is_vandalism(comment):
    words = re.compile('vandal')
    if words.search(comment): 
        return True
    else:
        return False

def savePage(title, chains, id, weight, longest):
    path = f"{output}wars_{id%4}.json"
    dump_out = open(path, 'a')

    filesize = os.path.getsize(path)
    if filesize == 0:
        dump_out.write('[')

    
    dump_out.write(json.dumps({'title': title, 'chains': chains, 'mean': weight, 'longest': longest})+',')
    dump_out.close()


def finish_files():
    for filename in os.listdir(output):
        print(filename)
        dump_out = open(output+filename, 'a')
        dump_out.write('{}]') # andrebbe cancellata la virgola, uso questo trick per farlo sintatticamente corretto

def get_DataFrame():

    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()
    df =[]
    

    while line != '':
 
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        df.append(values)

    return pd.DataFrame(df)


#%%




# %% COMPLEX 
inizio = datetime.now()
c_chains = complex_chains()
sorted(c_chains, key=lambda k: len(c_chains[k]), reverse=True)
print(datetime.now() -inizio)




# %% SIMPLE
inizio = datetime.now()
s_chains, stats = simple_chains()
sorted(s_chains, key=lambda k: len(s_chains[k]), reverse=True)
sorted(stats.items(), key=lambda k: k[1][1], reverse = True) # catena piu lunga
sorted(stats.items(), key=lambda k: k[1][0], reverse = True) # media
print(datetime.now() -inizio)



#%% sort pages by revert number

df = get_DataFrame()    
df = df.filter([3,4,7,25,34,64,67], axis = 1) 
df.columns = ['timestamp','commento', 'utente','pagina' , 'edit_count','reverted', 'reverta' ]
df_by_page = df.groupby(['pagina']).count().sort_values(by=['utente'], ascending=False)


# %%

# %%










#%% non so perchè ma non funziona o  forse noon funziona l'altro 


# %%
