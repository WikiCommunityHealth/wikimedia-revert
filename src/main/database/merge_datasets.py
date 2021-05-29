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

mut_df = pd.read_csv(file, sep='\t').groupby(['user','year_month']).sum()
rev_df = pd.read_csv(file2, sep='\t', index_col=(['user','year_month']))



merged_df = pd.concat([rev_df,mut_df ], axis=1)
merged_df = merged_df.fillna(0)
merged_df.to_csv(output, sep="\t")


# %% pages 
file = '/home/gandelli/dev/data/admin/pages/mutuals.tsv'
file2 = '/home/gandelli/dev/data/admin/pages/reverts.tsv'

output = '/home/gandelli/dev/data/admin/pages/all.tsv'

mut_df = pd.read_csv(file, sep='\t')
rev_df = pd.read_csv(file2, sep='\t')



merged_df = pd.concat([rev_df,mut_df ], axis=1)
merged_df.fillna(0)
merged_df.to_csv(output, sep="\t")




# %%
