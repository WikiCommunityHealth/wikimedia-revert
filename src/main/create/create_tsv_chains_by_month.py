
#%%
# PAGE EXAMPLE
# {'title': 'Zuppa_di_pesce_(film)',
#  'chains': [{'revisions': ['95861493', '95861612', '95973728'],
#    'users': {'93.44.99.33': '', 'Kirk39': '63558', 'AttoBot': '482488'},
#    'len': 3,
#    'start': '2018-04-01 04:54:40.0',
#    'end': '2018-04-05 07:36:26.0'}],
#  'n_chains': 1,
#  'n_rev_in_chainerts': 3,
#  'mean': 3.0,
#  'longest': 3,
#  'M': 0,
#  'lunghezze': {'3': 1}}

import json
from datetime import datetime
import numpy as np
import pandas as pd
from utils import utils 


dataset_folder_pages = '/home/gandelli/dev/data/wars_json/pages/'
dataset_folder_users = '/home/gandelli/dev/data/wars_json/users/'

output_pages = '/home/gandelli/dev/data/monthly/pages/chains.tsv'
output_users = '/home/gandelli/dev/data/monthly/users/chains.tsv'

out_pages = open(output_pages, 'w')
out_pages.write('titolo\tmonth\tnchain\tnrev_chain\tmean\tlongest\tmore_than5\tmore_than7\tmore_than9\tG\tinvolved\n')

out_users = open(output_users, 'w')
out_users.write('user\tmonth\tnchain\tnrev_chain\tmean\tlongest\tmore_than5\tmore_than7\tmore_than9\tG\tinvolved\n')

pagine = 0

#%%
def main():
    inizio = datetime.now()
    print(inizio.strftime(" %H:%M:%S"))
    read_json(dataset_folder_pages)             # compute pages 
    print('pagine fatte', datetime.now() - inizio)
    read_json(dataset_folder_users)             # compute users
    print('utenti fatti', datetime.now() - inizio)
    

def read_json(path):
    i = 10 # number of files in the wars folder
    #pages
    for i in range (0,i):
        dump_in = open(f"{path}wars_{i}.json")
        line = dump_in.readline()
        while(line != ''):
            line = dump_in.readline()
            if line == '{}]' or line == '':
                continue
            page = json.loads(line[:-2]) # it's called page but could be also an user 
            by_month(page)


# slit up by month the page
def by_month(page):
    current_year_month = ''
    n_chain = 0
    n_rev_in_chain = 0
    longest = 0
    more_than = np.zeros(10)
    chains = []
    utenti = []
   

    #use the start date of the chain to slit up by month
    for chain in page['chains']:

        date = datetime.strptime(chain['start'], '%Y-%m-%d %H:%M:%S.%f')
        year_month = str(date.year) +'-'+ str(date.month)
        n_chain +=1
        n_rev_in_chain += chain['len']
        longest = max(longest,chain['len'])
        chains.append(chain)
         

        #count the number of the chain greater than 5,7,9 
        for i in (5,7,9):
            if(chain['len'] >= i):
                more_than[i] += 1

        #
        for utente in list(chain['users']):
                utenti.append(utente)
        
        #at the end of the month save a line 
        if year_month != current_year_month:
            mean = round(n_rev_in_chain/n_chain, 1)
            G,involved = utils.getG(chains)
            
            if 'title' in page:
                save_page(page['title'], year_month, n_chain, n_rev_in_chain, mean, longest, int(more_than[5]),int(more_than[7]),int(more_than[9]), G, involved)
            elif 'user' in page:
                save_user(page['user'], year_month, n_chain, n_rev_in_chain, mean, longest, int(more_than[5]),int(more_than[7]),int(more_than[9]), G, involved)
            
            current_year_month = year_month
            n_chain = 0
            n_rev_in_chain = 0
            mean = 0
            longest = 0
            more_than = np.zeros(10)
            chains = []
            # all the users a user reverted 
    
    df = pd.DataFrame(utenti)
    grouped = df.groupby([0])[0].count().reset_index(name="count").sort_values('count', ascending = False)

def save_page(title, year_month, n_chain, n_rev_in_chain, mean, longest, more5, more7, more9, G, involved):
    out_pages.write(f'{title}\t {year_month}\t {n_chain}\t {n_rev_in_chain}\t {mean}\t {longest}\t {more5}\t {more7}\t {more9}\t {G}\t {involved}\n')
    #print(title, year_month, n_chain, n_rev_in_chain, mean, longest)

def save_user(user, year_month, n_chain, n_rev_in_chain, mean, longest, more5, more7, more9, G, involved):
    out_users.write(f'{user}\t {year_month}\t {n_chain}\t {n_rev_in_chain}\t {mean}\t {longest}\t {more5}\t {more7}\t {more9}\t {G}\t {involved}\n')

  


# %%
main()
# %%
