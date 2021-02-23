# %% intro
import bz2
import pandas as pd
from datetime import datetime

dataset = '/home/gandelli/dev/data/it/filtered_sorted_it.tsv.bz2'
#dataset = '/home/gandelli/dev/data/it/conte20.tsv'

#l'ultima colonna è fals invece che false 



#%% functions 

def complex_chains(page):
    open_chains = []
    complete_chains = []

    #dump_in = bz2.open(dataset, 'r')
    dump_in = open(dataset, 'r')
    line = dump_in.readline()

    inizio = datetime.now()
    i = 0

    while line != '':
        
        i+=1
        if i%10000 == 0:
            print(datetime.now()-inizio)
            

        #line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        line = dump_in.readline().rstrip()[:-1]

        values = line.split('\t')

        if line == '':
            continue

        if len(values) < 69:
            continue

        
        
        page_name = values[25]
        rev_id = values[52]
        reverter = values[65]
        is_reverted = values[64]
        added = False
        exist = False

    
        
        #check if this revision is part of a chain
        if page_name == page:
            for chain in open_chains: 

                for i in range(len(chain)):
                    if chain[i] == reverter:
                        exist = True

                if chain[-1] == rev_id:                                 # if the last element of the chain match with the current revision id
                    added = True
                    if is_reverted == 'true' and not exist:                           # continue the chain
                        chain.append(reverter) 
                    else:                                               # end of the chain this revision is not reverted 
                        if len(chain) > 1 :
                            complete_chains.append(chain)
                        open_chains.remove(chain)                       
           

            if not added and not exist:
                print('new catena', reverter)
                open_chains.append([reverter])
        
    return complete_chains

def simple_chains():

    
    dump_in = bz2.open(dataset, 'r')
    

    line = dump_in.readline()
    inizio = datetime.now()
    i = 0

    reverter_id = 0
    chains = []
    chain = []
    page = ''
    page_chains = {}
    while line != '':
       
        i+=1
        if i%100000 == 0:
            print(datetime.now()-inizio)

        
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        if line == '':
            continue
        
        
        
        page_name = values[25]
        rev_id = values[52]
        reverter = values[65]
        is_reverted = values[64]

        if page_name == page:

            if rev_id == reverter_id:
                chain.append(rev_id)
            else:
                if len(chain) > 1:
                    chains.append(chain)
                chain = []


            if is_reverted == 'true':
                reverter_id = reverter # save the value fot the next loop
        else:
            
            if(len(chains) > 0):
                page_chains[page] = chains
            page = page_name    
            chains = [] 

    return page_chains

def get_DataFrame():

    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()
    df =[]
    

    while line != '':
 
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        df.append(values)

    return pd.DataFrame(df)

#%% sort pages by revert number

df = get_DataFrame()    
df = df.filter([3,4,7,25,34,64,67], axis = 1) 
df.columns = ['timestamp','commento', 'utente','pagina' , 'edit_count','reverted', 'reverta' ]
df_by_page = df.groupby(['pagina']).count().sort_values(by=['utente'], ascending=False)
#%%

#dovrebbe ordinare le pagine per numero di revert
# le revisioni che sono revert

# %%
 
conte_chains = complex_chains('Governo_Conte_II')



# %%

s_chains = simple_chains()
sorted(s_chains, key=lambda k: len(s_chains[k]), reverse=True)



# %%
