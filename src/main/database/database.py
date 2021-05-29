import psycopg2


class DatabaseHelper:

    def __init__(self) -> None:
        print('initialized')
        self.connection =  psycopg2.connect(dbname='postgres', user='root', host='localhost', password='root', port='5420')

    def query(self, sql):
        con = self.connection
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        print('table created')

    def insert_from_file(self, path):
        con = self.connection
        cur = con.cursor()
        f = open(path, 'r')
        print('uploading '+ path.split('/')[-1], '...')
        cur.copy_from(f, 'revert_user', sep='\t')
        print('uploaded '+ path.split('/')[-1])
        con.commit()

    def dropTable(self, table_name):
        con = self.connection
        cur = con.cursor()
        print('dropping table', table_name)
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        con.commit()
        cur.close()


