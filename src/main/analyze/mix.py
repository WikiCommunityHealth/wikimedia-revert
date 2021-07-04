#%%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr

file = '/home/gandelli/dev/data/ca/admin/user/reverts.tsv'

df = pd.read_csv(file, sep='\t')[['user','year_month','tot_done', 'tot_received']]
df['year_month'] = pd.to_datetime(df.year_month)

# %%
folder = '/home/gandelli/dev/data/ita/chains/month/'

dfc = pd.read_csv(folder + 'user.tsv', sep='\t')[['user','month','nchain']]
dfc= dfc.rename(columns={'month': 'year_month'})
dfc['year_month'] = pd.to_datetime(dfc.year_month)

#%% chains joined by month for a specific user 
def plot_user_chain_by_month(user):
    a = df[df['user'] == user]
    b = a.groupby('year_month').count()

    plt.style.use('bmh')
    ax = b['user'].plot.bar(figsize=(25,5), fontsize=20)
    ax.set_xticks(ax.get_xticks()[::12])
    plt.gcf().autofmt_xdate()
    plt.title('Juan')
    ax.legend(['number of chains joined'],fontsize=20)
    plt.savefig('/home/gandelli/dev/data/plots/chains_user_month.png', dpi=300, bbox_inches='tight')


plot_user_chain_by_month('CristianCantoro')
# %%
