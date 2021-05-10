#%%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr

file = '/home/gandelli/dev/data/monthly/users/reverts.tsv'

df = pd.read_csv(file, sep='\t')
df['year_month'] = pd.to_datetime(df.year_month)


# %%
grouped = df.groupby(['user','group'], as_index=False).sum()
grouped.sort_values('tot_received', ascending=False)[:20]
grouped.sort_values('tot_done', ascending=False)[:20]



# %%
def get_user(user):

    plt.style.use('seaborn')
    utente = df[df['user'] == user]
    utente[['tot_received']]
    plt.figure(figsize=(15,8))
    plt.plot(utente['year_month'], utente[['tot_received', 'tot_done']])
    plt.legend(['tot_received', 'tot_done'])
# %% revert received and done 
grouped = df.groupby('year_month',  as_index=False).sum()
plt.figure(figsize=(15,8))
plt.plot(grouped['year_month'], grouped[['tot_received', 'tot_done']])
plt.legend(['tot_received', 'tot_done'])

#%% revert done 
plt.figure(figsize=(15,8))
plt.plot(grouped['year_month'], grouped[[ 'tot_done','d_not', 'd_reg', 'd_adm']])
plt.legend(['tot_done', 'done_by_anon', 'done_by_registered', 'done_by_admin'])


# %% revert received
plt.figure(figsize=(15,8))
plt.plot(grouped['year_month'], grouped[[ 'tot_received','r_not', 'r_reg', 'r_adm']])
plt.legend(['tot_received', 'received_by_anon', 'received_by_registered', 'received_by_admin'])
# %%
