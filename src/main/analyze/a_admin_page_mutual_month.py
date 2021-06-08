#%%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr

file = '/home/gandelli/dev/data/admin/page/mutuals.tsv'

df = pd.read_csv(file, sep='\t', index_col=['page_id' ])
df.dropna()
df['page_name']= df['page_name'].astype(str)
df = df[~df['page_name'].str.contains(r'\\', na = False)]

#df['year_month'] = pd.to_datetime(df.year_month).dt.date
# %%
df.groupby('page_name')['M'].max()


#a = df[df['page_name'] == 'Laura_Pausini']

a = df.groupby('page_name')['M'].sum()




a# %%

# %%
