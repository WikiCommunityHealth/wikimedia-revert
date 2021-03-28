# %%
import pandas as pd
import matplotlib.pyplot as plt
import csv

folder = '/home/gandelli/dev/data/monthly/'

df = pd.read_csv(folder + 'all.tsv', sep='\t')
df['month'] =pd.to_datetime(df.month)

# %% number of page that have at least one chain for each month  
grouped = df.groupby('month').count().sort_values('month')
grouped['titolo'].to_csv(folder + 'grouped_by_month.tsv', sep="\t", quoting=csv.QUOTE_NONE)

plt.style.use('seaborn')
grouped['titolo'].plot()


# %% number of months that a page has at least a chain 
grouped = df.groupby('titolo').count().sort_values('month', ascending = False)
grouped['month'].to_csv(folder + 'grouped_by_page_sorted.tsv', sep="\t", quoting=csv.QUOTE_NONE)


# %%
