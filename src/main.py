#%%
import bz2
import pandas as pd
from datetime import datetime


#l'ultima colonna è fals invece che false 
dump_in = bz2.open('./data/sorted.tsv.bz2', 'r')
line = dump_in.readline()

inizio = datetime.now()
df =[]
#TEMPO 
#!! dataframe estrarre solo dati interessanti
#cercare pagine controverse in base ai cluster di revert 
# capire chi è il revertato e ricostruire catene 
#aggiungere i revertati al df

 #TODO: usare un altro dataset 


output = open('principala.tsv', "w")

#%%
#creo il dataframe 
i=0
while line != '':
    i+=1
    if i%100000 == 0:
        print(datetime.now()-inizio)

    line = dump_in.readline().rstrip().decode('utf-8')[:-1]
    values = line.split('\t')

    if values[25] =='Pagina_principala':
        output.write(line+ '\n')

    df.append(values)


df = pd.DataFrame(df)

#%%

#dovrebbe ordinare le pagine per numero di revert
# le revisioni che sono revert
df = df.filter([3,4,7,25,34,64,67], axis = 1) 
df.columns = ['timestamp','commento', 'utente','pagina' , 'edit_count','reverted', 'reverta' ]
df_by_page = df.groupby(['pagina']).count().sort_values(by=['utente'], ascending=False)
# %%
