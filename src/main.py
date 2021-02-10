#%%
import bz2
import pandas as pd
from datetime import datetime


#l'ultima colonna è fals invece che false 
dump_in = bz2.open('/Users/alessiogandelli/wikipedia/lombardo.tsv.bz2', 'r')
line = 'something'
line = dump_in.readline()

title = 'Carboni'
df = []
i = 0

inizio = datetime.now()

#TEMPO 
#!! dataframe estrarre solo dati interessanti
#cercare pagine controverse in base ai cluster di revert 
# capire chi è il revertato e ricostruire catene 
#aggiungere i revertati al df

 #TODO: FARE SORT DEL DATASET PER PAGINA e usare un altro dataset 

#%%
while line != '':
    i+=1
    if i%100000 == 0:
        print(datetime.now()-inizio)

    line = dump_in.readline().rstrip().decode('utf-8')[:-1]
    values = line.split('\t')

    if len(values) < 3:      
        continue

    if values[1] != 'revision':
        continue


    # se è un revert aggiungi 
   # if values[67] == 'true':
        #print(line)

    df.append(values)

    # event_entity = values[1]
    # event_user_id = values[5]
    # try: int(event_user_id)
    # except: 
    #     continue
    # page_title = values[25]
    # page_id = values[23]
    # #edit_count = values[34]
    #is_revert = values[67]
   # print(values)

df = pd.DataFrame(df)
#%%

#dovrebbe ordinare le pagine per numero di revert
revert_df = df[df[67]== 'true'] # le revisioni che sono revert
revert_df_filtered = revert_df.filter([3,4,7,25,34,64,67], axis = 1) 
revert_df_filtered.columns = ['timestamp','commento', 'utente','pagina' , 'edit_count','reverted', 'reverta' ]
sorted_by_revert_df = revert_df_filtered.groupby(['pagina']).count().sort_values(by=['utente'], ascending=False)
# %%
