#%%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr

folder = '/home/gandelli/dev/data/monthly/users/'

df = pd.read_csv(folder + 'all.tsv', sep='\t')
df['month'] = pd.to_datetime(df.month).dt.date

#%% chains joined by month for a specific user 
def plot_user_chain_by_month(user):
    a = df[df['user'] == user]
    b = a.groupby('month').count()

    plt.style.use('seaborn')
    ax = b['user'].plot.bar(figsize=(25,5))
    ax.set_xticks(ax.get_xticks()[::12])
    plt.gcf().autofmt_xdate()
    plt.title(user)

plot_user_chain_by_month('Vituzzu')
# %%
