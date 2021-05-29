
#%%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr

file = '/home/gandelli/dev/data/admin/user/mutuals.tsv'
file2 = '/home/gandelli/dev/data/admin/user/reverts.tsv'

mut_df = pd.read_csv(file, sep='\t')
rev_df = pd.read_csv(file2, sep='\t')

df_user_month = df.groupby(['user','year_month']).sum().sort_values('mutual_with_admin')
# %%
