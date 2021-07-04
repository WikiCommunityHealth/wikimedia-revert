#%%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr

folder = '/home/gandelli/dev/data/es/admin/page/'
file = 'reverts.tsv'
mutual = 'mutuals.tsv'


df = pd.read_csv(folder + file, sep='\t').dropna()
df_mut =pd.read_csv(folder + mutual, sep='\t').dropna()

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
dfg = dfg[['reg_reg', 'adm_reg','reg_adm', 'adm_adm']]
dfg.plot()
plt.title('spanish')
plt.savefig('/home/gandelli/dev/data/plots/admin_es.png', dpi=300, bbox_inches='tight')

# %%


df['year_month'] = pd.to_datetime(df.year_month)
grouped = df.groupby('year_month', as_index=False).count().sort_values('year_month')
plt.figure(figsize=(15,8))
x = month_abbr[1:13]
for i in range(2010,2021):
    plt.plot(x,grouped[grouped['year_month'].dt.year == i]['reg_reg'], label = i)

plt.legend()
plt.title('catalan ')
plt.savefig('/home/gandelli/dev/data/plots/admin_year_ca.png', dpi=300, bbox_inches='tight')

# %%
