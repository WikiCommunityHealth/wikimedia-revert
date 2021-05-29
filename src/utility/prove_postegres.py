#%%
import psycopg2

con = psycopg2.connect(dbname='postgres', user='root', host='localhost', password='root', port='5420')

cur = con.cursor()

cur.execute("insert into players values ('beppe', 420)")

cur.execute("select * from players")


rows = cur.fetchall()

for r in rows:
    print(r)

cur.close()

con.close()
# %%
