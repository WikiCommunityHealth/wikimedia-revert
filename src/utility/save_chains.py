#%%
import bz2
import pandas as pd
from datetime import datetime
import json

#dataset = '/home/gandelli/dev/data/it/filtered_sorted_it.tsv.bz2'
dataset = '/home/gandelli/dev/data/test/magalli.tsv'
output = '/home/gandelli/dev/data/test/wars.json'

def complex_chains():
    

    #dump_in = bz2.open(dataset, 'r') 
    dump_in = open(dataset, 'r')# for uncompressed 
    dump_out = open('wars.json', 'w')
    line = dump_in.readline()


    inizio = datetime.now()


    #variables
    open_chains = []
    complete_chains = []
    users = []
    current_page = ''
    page_chains = {}

    page_json = {
        "page": 'titolo',
        "wars": []

    }

    war_json = {
        "users": ['pippo', 'pluto'],
        "revisions": []
    }

    page_wars_json = []

    #for every line of the dataset
    while line != '':
        
       # line = dump_in.readline().rstrip().decode('utf-8')[:-1] 
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


        if page_name == 'Giancarlo_Magalli':
            pass
            #print(rev_id, reverter, is_reverted)

      
        #check if this revision is part of a chain
        if page_name != current_page: # new page 
            
            if(len(complete_chains) > 0):   #save the last page 
               
                #page_json['page'] = current_page   
                #page_json['wars'] = page_wars_json
                page_chains[current_page] = complete_chains  #dict  
                
                #print(open_chains)
                #dump_out.write(json.dumps(page_json))
                #dump_out.write(',\n')

            current_page = page_name

            page_json = {}
            page_wars_json = {}

            complete_chains = []
            open_chains = []
        
        else:   #continue page 
            for chain in open_chains:                                   

                exist = is_rev_in_chain(reverter, chain)
                if exist:
                    continue                                                    #if it already exist i'm not interested in this chain
                      
                        
                if chain[-1] == rev_id:                                        #if the last element of the chain match with the current revision id
                    added = True
                    if is_reverted == 'true' :                           # continue the chain
                        chain.append(reverter)
 
                    else:                                               # end of the chain this revision is not reverted 
                        if len(chain) > 2 :
                            complete_chains.append(chain)
                        open_chains.remove(chain)                       
           

            if not added and not exist and is_reverted == 'true':
                
                open_chains.append([rev_id, reverter])          # new chain if the reverter does not already exist in  open_chains

    return page_chains

def is_rev_in_chain(reverter, chain):
     for i in range(len(chain)):                             # if the one you want to insert already exists don't add it 
        if chain[i] == reverter:
            return True
     return False                   
# %%

cc = complex_chains()
sorted(cc, key=lambda k: len(cc[k]), reverse=True)
# %%


def simple_chains():

    #dump_in = bz2.open(dataset, 'r')
    dump_in = open(dataset, 'r')# for uncompressed 
    line = dump_in.readline()
    

    reverter_id = 0
    chains = []
    chain = []
    current_page = ''
    page_chains = {}
    users = set()
    
    while line != '':

        
        #line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        line = dump_in.readline().rstrip()[:-1]# for uncompressed 
        values = line.split('\t')

        if line == '' or values[28] != '0' or is_vandalism(values[4]): # i want only namespace 0 and no vandalism
            continue

        
        
        page_name   = values[25]
        rev_id      = values[52]
        reverter    = values[65]
        is_reverted = values[64]
        user        = values[7]

        if page_name != current_page:                           #
            if(len(chains) > 0):
                savePage(current_page, chains)
                page_chains[current_page] = chains
            current_page = page_name    
            chains = [] 
           
             
        else:

            if rev_id == reverter_id:                                   #if the currect reverts the previous one
                chain.append(rev_id)     
                users.add(user)                               # continue the chain
            else:
                if len(chain) > 2:
                    chains.append({'revisions':chain, 'users' : list(users)})
                chain = [rev_id]
                users = {user}
                

            if is_reverted == 'true':
                reverter_id = reverter # save
            

    return page_chains

import re



def is_vandalism(comment):
    words = re.compile('vandal')
    if words.search(comment): 
        return True
    else:
        return False

def savePage(title, chains):
    dump_out = open(output, 'w')
    dump_out.write(json.dumps({'title': title, 'chains': chains}))
    dump_out.close()

simple_chains()

# %%
