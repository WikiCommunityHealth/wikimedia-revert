#%%
from database import DatabaseHelper




#%% revert user 

sql_create_revert_user = """CREATE TABLE public.revert_user(
                 ilcapo bigint,name text,yearmonth text,role text,tot_received double precision,r_reg double precision,r_not double precision,r_adm double precision,tot_done double precision,d_reg double precision,d_not double precision,d_adm double precision,mutual_with_admin double precision,mutual_with_reg double precision,mutual_with_not double precision,
                  CONSTRAINT revert_user_pkey PRIMARY KEY ( ilcapo, name, yearmonth))"""


path = '/home/gandelli/dev/data/admin/user/all.tsv'
db = DatabaseHelper()
db.dropTable('revert_user')
db.query(sql_create_revert_user)
db.insert_from_file(path, 'revert_user')

#%% revert pages

sql_create_revert_page = """CREATE TABLE public.revert_page(
                  ilcapo bigint, page_id bigint, name text,yearmonth text,adm_adm double precision, adm_reg double precision,reg_adm double precision,reg_reg double precision,not_reg double precision,reg double precision,mut_adm_adm double precision,mut_adm_reg double precision,mut_reg_reg double precision,mut_not_reg double precision,mut_reg double precision,
                  CONSTRAINT revert_page_pkey PRIMARY KEY ( ilcapo,page_id,name, yearmonth))"""


path = '/home/gandelli/dev/data/admin/page/all.tsv'
db = DatabaseHelper()
db.dropTable('revert_page')
db.query(sql_create_revert_page)
db.insert_from_file(path, 'revert_page')
# %%
 