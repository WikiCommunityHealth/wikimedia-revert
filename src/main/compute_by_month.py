
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


dataset_folder = '/home/gandelli/dev/data/wars/'
output = '/home/gandelli/dev/data/montly_stats.tsv'

out = open(output, 'w')
print(out.write('titolo\tmonth\tnchain\tnrev\tmean\tlongest\n'))


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
    for chain in page['chains']:

        date = datetime.strptime(chain['start'], '%Y-%m-%d %H:%M:%S.%f')
        year_month = str(date.year) +'-'+ str(date.month)
        n_chain +=1
        n_rev += chain['len']
        longest = max(longest,chain['len'])
        #M = 0

        if year_month != current_year_month:
            mean = round(n_rev/n_chain, 1)
            save(page['title'], year_month, n_chain, n_rev, mean, longest)
            
            current_year_month = year_month
            n_chain = 0
            n_rev = 0
            mean = 0
            longest = 0
            #M = 0



def save(title, year_month, n_chain, n_rev, mean, longest):
    out.write(f'{title}\t {year_month}\t {n_chain}\t {n_rev}\t {mean}\t {longest}\n')
    #print(title, year_month, n_chain, n_rev, mean, longest)

# %%
main()
# %%
