#%%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr

folder = '/home/gandelli/dev/data/ca/chains/month/'

df = pd.read_csv(folder + 'user.tsv', sep='\t')
df['month'] = pd.to_datetime(df.month).dt.date

#%% chains joined by month for a specific user 
def plot_user_chain_by_month(user):
    a = df[df['user'] == user]
    b = a.groupby('month').count()

    plt.style.use('bmh')
    ax = b['user'].plot.bar(figsize=(25,5), fontsize=20)
    ax.set_xticks(ax.get_xticks()[::12])
    plt.gcf().autofmt_xdate()
    plt.title('Juan')
    ax.legend(['number of chains joined'],fontsize=20)
    plt.savefig('/home/gandelli/dev/data/plots/chains_user_month.png', dpi=300, bbox_inches='tight')


plot_user_chain_by_month('CarlesMartin')

# %%
