#%%
import pandas as pd
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr
# %% 

#user 
file = '/home/gandelli/dev/data/admin/user/mutuals.tsv'
file2 = '/home/gandelli/dev/data/admin/user/reverts.tsv'

output = '/home/gandelli/dev/data/admin/user/all.tsv'

print('parsing users from file...')
mut_df = pd.read_csv(file, sep='\t').groupby(['user','year_month']).sum()
rev_df = pd.read_csv(file2, sep='\t', index_col=(['user','year_month']))


print('merging...')
merged_df = rev_df.merge(mut_df, on=['user','year_month'], how='left').fillna(0).reset_index()
merged_df = merged_df[~merged_df['user'].str.contains(r'\\', na = False)]
print('saving...')
merged_df.to_csv(output, sep="\t",header=False)
print('saved')



# %% pages 
file1 = '/home/gandelli/dev/data/admin/page/mutuals.tsv'
file2 = '/home/gandelli/dev/data/admin/page/reverts.tsv'

output = '/home/gandelli/dev/data/admin/page/all.tsv'

print('parsing pages from file...')
mut_df = pd.read_csv(file1, sep='\t')
rev_df = pd.read_csv(file2, sep='\t')
rev_df = rev_df[~rev_df['page_name'].str.contains(r'\\|1764604', na = False)].dropna()
rev_df = rev_df[~rev_df.index.duplicated(keep='first')]

print('merging...')
merged_df = rev_df.merge(mut_df, on=['page_id', 'page_name','year_month'], how='left').fillna(0).reset_index()
print('saving...')
merged_df.to_csv(output, sep="\t", header = False, index = False)
print('saved')

#levare intestazione 

# %%
