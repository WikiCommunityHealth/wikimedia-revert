#%%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr

folder = '/home/gandelli/dev/data/pages_data/'
file = 'reverts_admin.tsv'
mutual = 'mutual_reverts_admin.tsv'


df = pd.read_csv(folder + file, sep='\t')

df['not_rev_on_total'] = df['not_reg']/ (df['not_reg'] + df['reg'])
df['rev_on_total'] = df['reg']/ (df['not_reg'] + df['reg'])
df['total_reverts'] = df['reg'] + df['not_reg']

#%% some sorting 
df.sort_values('reg', ascending=False)[:20]
df.sort_values('not_reg', ascending=False)[:20]
df.sort_values('reg_reg', ascending=False)[:20]
df.sort_values('reg_adm', ascending=False)[:20]
df.sort_values('adm_reg', ascending=False)[:20]
df.sort_values('adm_adm', ascending=False)[:20]


#%%  groupby number of reverts in different bins

labels = ['0', '1', '2-4', '5-9', '10-99', '100-9999']
bins = pd.cut(df['total_reverts'], [0,1,2,5, 10, 100, 10000], right=False, labels = labels)
df.groupby(bins)['total_reverts'].agg(['count', 'sum'])


#%% m

df = pd.read_csv(folder + mutual, sep='\t')

# %%
