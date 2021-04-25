# %%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr

folder = '/home/gandelli/dev/data/monthly/pages/'


df_rev = pd.read_csv(folder + 'reverts.tsv', sep='\t')
df = pd.read_csv(folder + 'chains.tsv', sep='\t')
df['month'] =pd.to_datetime(df.month)


#CHAINS
# %% number of page that have at least one chain for each month  
grouped = df.groupby('month').count().sort_values('month')
grouped['titolo'].to_csv(folder + 'grouped_by_month.tsv', sep="\t", quoting=csv.QUOTE_NONE)

plt.style.use('seaborn')
grouped['titolo'].plot()
plt.savefig('/home/gandelli/dev/data/plots/page_per_chain_global.png', dpi=300, bbox_inches='tight')


# the same of above but one line per year 
grouped = df.groupby('month', as_index=False).count().sort_values('month')
plt.figure(figsize=(15,8))
x = month_abbr[1:13]
for i in range(2010,2021):
    plt.plot(x,grouped[grouped['month'].dt.year == i]['titolo'], label = i)

plt.savefig('/home/gandelli/dev/data/plots/page_per_chain_by_year.png', dpi=300, bbox_inches='tight')

# %% number of months that a page has at least a chain 
grouped = df.groupby('titolo').count().sort_values('month', ascending = False)
grouped['month'].to_csv(folder + 'grouped_by_page_sorted.tsv', sep="\t", quoting=csv.QUOTE_NONE)


# %% pages which have >2 chains longer than 9 sorted by controversiality
df[df['more_than9'] > 2].sort_values('M', ascending=False)


#REVERTS
# %% reverts by month
plt.style.use('seaborn')
grouped = df_rev.groupby('year_month').sum()
ax = grouped['nrev'].plot(figsize=(15,5))
plt.title('number of reverts by month')
# %%

df_rev['year_month'] = pd.to_datetime(df_rev['year_month'])
grouped = df_rev.groupby('year_month', as_index=False).sum().sort_values('year_month')
plt.figure(figsize=(15,8))
x = month_abbr[1:13]
for i in range(2010,2021):
    plt.plot(x,grouped[grouped['year_month'].dt.year == i]['nrev'], label = i)


# %%
