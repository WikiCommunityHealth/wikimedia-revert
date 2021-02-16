# %%
import bz2
import pandas as pd
from datetime import datetime

dataset = '/home/gandelli/dev/venv/dataset/sorted.tsv.bz2'


#l'ultima colonna è fals invece che false 

#%% dati utili 

inizio = datetime.now()



#creo il dataframe 
def get_DataFrame():

    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()
    df =[]
    

    while line != '':
 
        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        df.append(values)

    return pd.DataFrame(df)

df = get_DataFrame()    

df = df.filter([3,4,7,25,34,64,67], axis = 1) 
df.columns = ['timestamp','commento', 'utente','pagina' , 'edit_count','reverted', 'reverta' ]
df_by_page = df.groupby(['pagina']).count().sort_values(by=['utente'], ascending=False)
#%%

#dovrebbe ordinare le pagine per numero di revert
# le revisioni che sono revert

# %%


def complex_chains(page):
    open_chains = []
    complete_chains = []

    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()

    inizio = datetime.now()
    i = 0

    while line != '':
        
        i+=1
        if i%10000 == 0:
            print(datetime.now()-inizio)
            

        line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        values = line.split('\t')

        if line == '':
            continue

        page_name = values[25]
        rev_id = values[52]
        reverter = values[65]
        is_reverted = values[64]
        added = False

    
        
        #check if this revision is part of a chain
        if page_name == page:
            for chain in open_chains:
                if chain[-1] == rev_id:
                    added = True
                    if is_reverted == 'true':
                        chain.append(reverter) 
                    else:# catena finita 
                        if(len(chain) > 1):
                            complete_chains.append(chain)
                        open_chains.remove(chain) # controllare non si rompa
                        
            if not added:
                
                open_chains.append([reverter])
        
    return complete_chains
        
        
        
chains = complex_chains('Governo_Conte_II')



# %%

def simple_chains(page):

    dump_in = bz2.open(dataset, 'r')
    line = dump_in.readline()
    inizio = datetime.now()
    i = 0

    reverter_id = 0
    chains = []
    chain = []

    while line != '':
        
        i+=1
        if i%10000 == 0:
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

    return chains

chains = simple_chains('Roma')

# %%
