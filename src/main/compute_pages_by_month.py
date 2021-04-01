
#%%
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

import json
from datetime import datetime
import numpy as np
import pandas as pd


dataset_folder = '/home/gandelli/dev/data/wars/'
output = '/home/gandelli/dev/data/monthly/all.tsv'

out = open(output, 'w')
out.write('titolo\tmonth\tnchain\tnrev\tmean\tlongest\tmore_than5\tmore_than7\tmore_than9\tM\tinvolved\n')

pagine = 0

def main():
    
    
    i = 10 # number of files in the wars folder
    for i in range (0,i):
        dump_in = open(f"{dataset_folder}wars_{i}.json")
        line = dump_in.readline()
        while(line != ''):
            line = dump_in.readline()
            if line == '{}]' or line == '':
                continue
            page = json.loads(line[:-2])
            by_month(page)
       
       
            

def by_month(page):
    current_year_month = ''
    n_chain = 0
    n_rev = 0
    longest = 0
    more_than = np.zeros(10)
    chains = []
    utenti = []

    for chain in page['chains']:

        date = datetime.strptime(chain['start'], '%Y-%m-%d %H:%M:%S.%f')
        year_month = str(date.year) +'-'+ str(date.month)
        n_chain +=1
        n_rev += chain['len']
        longest = max(longest,chain['len'])
        chains.append(chain)

        for i in (5,7,9):
            if(chain['len'] >= i):
                more_than[i] += 1

        for utente in list(chain['users']):
                utenti.append(utente)
        
        if year_month != current_year_month:
            mean = round(n_rev/n_chain, 1)
            M,involved = getM(chains)
            
            
            save(page['title'], year_month, n_chain, n_rev, mean, longest, int(more_than[5]),int(more_than[7]),int(more_than[9]), M, involved)
            
            current_year_month = year_month
            n_chain = 0
            n_rev = 0
            mean = 0
            longest = 0
            more_than = np.zeros(10)
            chains = []
    
    df = pd.DataFrame(utenti)
    grouped = df.groupby([0])[0].count().reset_index(name="count").sort_values('count', ascending = False)



def save(title, year_month, n_chain, n_rev, mean, longest, more5, more7, more9, M, involved):
    out.write(f'{title}\t {year_month}\t {n_chain}\t {n_rev}\t {mean}\t {longest}\t {more5}\t {more7}\t {more9}\t {M}\t {involved}\n')
    #print(title, year_month, n_chain, n_rev, mean, longest)

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

    return ((tot * len(utenti)), str(utenti))    
# %%
main()
# %%
