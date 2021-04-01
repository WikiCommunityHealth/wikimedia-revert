
#%%
# PAGE EXAMPLE
# {'title': 'Zuppa_di_pesce_(film)',
#  'chains': [{'revisions': ['95861493', '95861612', '95973728'],
#    'users': {'93.44.99.33': '', 'Kirk39': '63558', 'AttoBot': '482488'},
#    'len': 3,
#    'start': '2018-04-01 04:54:40.0',
#    'end': '2018-04-05 07:36:26.0'}],
#  'n_chains': 1,
#  'n_reverts': 3,
#  'mean': 3.0,
#  'longest': 3,
#  'M': 0,
#  'lunghezze': {'3': 1}}

import json
from datetime import datetime
import numpy as np
import pandas as pd


dataset_folder = '/home/gandelli/dev/data/wars/'
output = '/home/gandelli/dev/data/monthly/users/all.tsv'

out = open(output, 'w')
out.write('user\tmonth\tnchain\tnrev\tmean\tlongest\tmore_than5\tmore_than7\tmore_than9\tM\tinvolved\n')
