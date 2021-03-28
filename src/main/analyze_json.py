
#%% import
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

# PAGE EXAMPLE
# {'title': 'Zuppa_di_pesce_(film)',
#  'chains': [{'revisions': ['95861493', '95861612', '95973728'],
#    'users': {'93.44.99.33': '', 'Kirk39': '63558', 'AttoBot': '482488'},
#    'len': 3,
#    'start': '2018-04-01 04:54:40.0',
#    'end': '2018-04-05 07:36:26.0'}],
#  'n_chains': 1,
#  'n_reverts': 3,
#  'mean': 3.0,
#  'longest': 3,
#  'M': 0,
#  'lunghezze': {'3': 1}}

output_folder = '/home/gandelli/dev/data/analyze_wars/'

# read jsons file 
dataset_folder = '/home/gandelli/dev/data/wars/'
i = 10 # number of files in the wars folder

pagine = 0

reverts = {}
chain_month = {}
mean = {}
utenti = []

for i in range (0,i):
    dump_in = open(f"{dataset_folder}wars_{i}.json")
    line = dump_in.readline()
    while(line != ''):
        line = dump_in.readline()
        if line == '{}]' or line == '':
            continue
        page = json.loads(line[:-2])

        reverts[page['title']] = page['longest']
        for chain in page['chains']:
            chain_month[chain['start']] = chain['len']
            mean[page['title']] = page['mean']
            for utente in list(chain['users']):
                utenti.append(utente)
        
        


# %% plot  number of pages that have n as longest chain

df = pd.DataFrame(reverts.items(), columns=['n_of_pages', 'longest_chain'])
df = df.groupby(['longest_chain']).count()
plt.style.use('seaborn')
df.plot.bar(figsize=(15,5), logy = True, legend='False')

df[0:10].plot.bar(figsize=(15,5))
df[5:15].plot.bar(figsize=(15,5))
df[10:20].plot.bar(figsize=(15,5))


#%% number of chains of reverts per month

df = pd.DataFrame(chain_month.items(),  columns=['timestamp', 'len'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.groupby(pd.Grouper(key='timestamp', freq='M')).count()
ax = df.plot.bar(figsize=(15,5))
#ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
ax.set_xticks(ax.get_xticks()[::12])
plt.gcf().autofmt_xdate()

plt.show()

#%% number of pages that have the (rounded) mean length of the chains

df = pd.DataFrame(mean.items(), columns=['title', 'mean'])
df = df.groupby(df['mean'].apply(lambda x: round(x, 0))).count()
plt.style.use('seaborn')
df['mean'].plot.bar(figsize=(15,5), logy = True)

#%% number or chains each member is involved

df = pd.DataFrame(utenti)
grouped = df.groupby([0])[0].count().reset_index(name="count").sort_values('count', ascending = False)
grouped.to_csv(output_folder + 'n_chain_joined.tsv', sep="\t", quoting=csv.QUOTE_NONE)

