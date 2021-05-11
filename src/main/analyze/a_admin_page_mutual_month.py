#%%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr

file = '/home/gandelli/dev/data/monthly/pages/mutual.tsv'

df = pd.read_csv(file, sep='\t')
#df['year_month'] = pd.to_datetime(df.year_month).dt.date
# %%
grouped = df.groupby('year_month').sum()
grouped[['reg','adm_adm', 'adm_reg', 'reg_reg']].plot()
grouped.sum()










# %%
