#%% analyze the json pages about chains 
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime

inizio = datetime.now()
print(inizio.strftime(" %H:%M:%S"))

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

output_folder = '/home/gandelli/dev/data/ca/chains/results/'

# read jsons file 
dataset_folder = '/home/gandelli/dev/data/en/chains/page/'
i = 10 # number of files in the wars folder

pagine = 0

reverts = {}
chain_month = {}
mean = {}
utenti = [] 



m_pages_df = []
reverts_df = []
nchains_df = []
serieA = {}
pino = {}

for i in range (0,i):
    dump_in = open(f"{dataset_folder}wars_{i}.json")
    line = dump_in.readline()
    while(line != ''):
        line = dump_in.readline()
        if line == '{}]' or line == '' or line == '{}]{}]':
            continue

        page = json.loads(line[:-2])
        
        m_pages_df.append({ 'title': page['title'], 'M': page['M'], 'G':  page['G']})
        reverts_df.append((page['title'], page['n_reverts'],page['n_reverts_in_chains']))
        nchains_df.append({ 'title': page['title'], 'n_chains' : page['n_chains'], 'longest': page['longest']})

        if page['title'] == 'Juventus_Football_Club':
            serieA = page
        
        if page['title'] == 'Matt_Dillon':
            pino = page

        reverts[page['title']] = page['longest']
        for chain in page['chains']:
            chain_month[chain['start']] = chain['len']
            mean[page['title']] = page['mean']
            for utente in list(chain['users']):
                utenti.append(utente)
        
        
print(datetime.now() - inizio)

#%% n of chains

df = pd.DataFrame(nchains_df, columns=['title', 'n_chains'])
df = df.sort_values('n_chains', ascending=False).head(15)
df


# %% plot  number of pages that have n as longest chain

df = pd.DataFrame(reverts.items(), columns=['n_of_pages', 'longest_chain'])
df = df.groupby(['longest_chain']).count()
plt.style.use('seaborn')
df.plot.bar(figsize=(15,5), logy = True, legend='False')
#plt.savefig('/home/gandelli/dev/data/plots/longest_chain.png', dpi=300, bbox_inches='tight')

df[0:10].plot.bar(figsize=(15,5))
#plt.savefig('/home/gandelli/dev/data/plots/longest_chain0_10.png', dpi=300, bbox_inches='tight')
df[5:15].plot.bar(figsize=(15,5))
#plt.savefig('/home/gandelli/dev/data/plots/longest_chain5_15.png', dpi=300, bbox_inches='tight')
df[10:20].plot.bar(figsize=(15,5))
#plt.savefig('/home/gandelli/dev/data/plots/longest_chain10_20.png', dpi=300, bbox_inches='tight')


#%% number of chains of reverts per month

df = pd.DataFrame(chain_month.items(),  columns=['timestamp', 'len'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.groupby(pd.Grouper(key='timestamp', freq='M')).count()
ax = df.plot.bar(figsize=(15,5))
#ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
ax.set_xticks(ax.get_xticks()[::12])
plt.gcf().autofmt_xdate()

#plt.savefig('/home/gandelli/dev/data/plots/chains_per_month.png', dpi=300, bbox_inches='tight')

plt.show()


#%% number of pages that have the (rounded) mean length of the chains

df = pd.DataFrame(mean.items(), columns=['title', 'mean'])
df = df.groupby(df['mean'].apply(lambda x: round(x, 0))).count()
plt.style.use('seaborn')
df['mean'].plot.bar(figsize=(15,5), logy = True)
#plt.savefig('/home/gandelli/dev/data/plots/page_mean.png', dpi=300, bbox_inches='tight')


#%% number or chains each member is involved

df = pd.DataFrame(utenti)
grouped = df.groupby([0])[0].count().reset_index(name="count").sort_values('count', ascending = False)
grouped.to_csv(output_folder + 'n_chain_joined.tsv', sep="\t", quoting=csv.QUOTE_NONE)


#%% compare m and g

#sorted_m_pages = sorted(m_pages, key=lambda k: k['M'], reverse=True)
df = pd.DataFrame(m_pages_df, columns=['title', 'M','G'])
df['rapporto'] = df['M'] /df['G']
df[0:30].plot.bar(figsize=(15,5), logy = True, legend='False')


# %% number of reverts that are and aren't in a chain  
reverts_df = pd.DataFrame(reverts_df, columns=['title', 'n_reverts', 'n_reverts_in_chains'])
reverts_df['rapporto'] = reverts_df['n_reverts_in_chains'] / reverts_df['n_reverts']
mean_rapporto = reverts_df['n_reverts_in_chains'].sum()/reverts_df['n_reverts'].sum()
reverts_df = reverts_df.sort_values('rapporto', ascending=False)
#reverts_df.to_csv(output_folder + 'reverts_chain.tsv', sep="\t", quoting=csv.QUOTE_NONE)


# %% per il numero di revert in chain e non 
df = pd.DataFrame(reverts_df, columns=['title', 'rev', 'inchain'])
df.sum()
# %%
df = pd.DataFrame(nchains_df)
df = df.sort_values('longest', ascending=False).head(15)
df
# %%
