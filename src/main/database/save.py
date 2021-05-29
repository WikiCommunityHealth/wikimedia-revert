#%%
from database import DatabaseHelper




#%% revert user 

sql_create_revert_user = """CREATE TABLE public.revert_user(
                  name text,yearmonth text,role text,tot_received double precision,r_reg double precision,r_not double precision,r_adm double precision,tot_done double precision,d_reg double precision,d_not double precision,d_adm double precision,mutual_with_admin double precision,mutual_with_reg double precision,mutual_with_not double precision,
                  CONSTRAINT revert_user_pkey PRIMARY KEY ( name, yearmonth))"""


path = '/home/gandelli/dev/data/admin/user/all.tsv'
db = DatabaseHelper()
db.dropTable('revert_user')
db.query(sql_create_revert_user)
db.insert_from_file(path)

#%% revert pages

