
#%%
# PAGE EXAMPLE
# {'title': 'Zuppa_di_pesce_(film)',
#  'chains': [{'revisions': ['95861493', '95861612', '95973728'],
#    'users': {'93.44.99.33': '', 'Kirk39': '63558', 'AttoBot': '482488'},
#    'len': 3,
#    'start': '2018-04-01 04:54:40.0',
#    'end': '2018-04-05 07:36:26.0'}],
#  'n_reverts': 3,
#  'mean': 3.0,
#  'longest': 3,
#  'M': 0,
#  'lunghezze': {'3': 1}}

import json

dataset_folder = '/home/gandelli/dev/data/wars/'
i = 10 # number of files in the wars folder

pagine = 0

reverts= {}


for i in range (0,i):
    dump_in = open(f"{dataset_folder}wars_{i}.json")
    line = dump_in.readline()
    while(line != ''):
        line = dump_in.readline()
        if line == '{}]' or line == '':
            continue
        page = json.loads(line[:-2])
        reverts[page['title']] = page['M']
        
        
# %%

# %%
ordinata = sorted(reverts.items(), key=lambda item: item[1], reverse = True)
out = open('/home/gandelli/dev/data/risultati/controversiality.txt', 'w')
for el in ordinata:
    out.write(el[0]+' '+ str(el[1])+ '\n')
# %%
