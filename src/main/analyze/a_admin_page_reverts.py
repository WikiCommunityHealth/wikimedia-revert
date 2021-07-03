#%%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr

folder = '/home/gandelli/dev/data/ca/admin/page/'
file = 'reverts.tsv'
mutual = 'mutuals.tsv'


df = pd.read_csv(folder + file, sep='\t').dropna()
#%%
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
maxdf = df.groupby('page_id').max()
labels = ['0', '1', '2-4', '5-9', '10-99', '100-9999']
bins = pd.cut(maxdf['total_reverts'], [0,1,2,5, 10, 100, 10000], right=False, labels = labels)
maxdf.groupby(bins)['total_reverts'].agg(['count', 'sum'])


#%% m

df = pd.read_csv(folder + mutual, sep='\t')

# %%
df.plot('year_month', 'adm_adm')
# %%
dfg = df.groupby('year_month').sum().drop(['page_id','not_reg','reg'],1)
dfg.plot()
# %%
