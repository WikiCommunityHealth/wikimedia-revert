from typing import Dict, Iterable, Tuple, List
import psycopg2
import psycopg2.extras

class DatabaseService:

    metrics: List[str]
    insertSqlNames: str
    bufferLen = 0
    buffer: Dict[str, List[List[float]]] = {}
    def __init__(self, metrics: Iterable[str]) -> None:
        self.__connection = psycopg2.connect("dbname='postgres' user='root' host='localhost' password='root'")
        self.metrics = self.__flatList__(map(lambda x: [f"{x}_ASS", f"{x}_NORM", f"{x}_ASS_ACC", f"{x}_NORM_ACC"], metrics))
        self.insertSqlNames = f"(ilcapo, name, yearmonth, {', '.join(self.metrics)}) VALUES (%s, %s, %s, {', '.join(map(lambda _: '%s', self.metrics))})"

    def __flatList__(self, list) -> List[str]:
        return [item for sublist in list for item in sublist]

    def createTable(self, tables: List[str]):
        cur = self.__connection.cursor()
        for t in tables:
            metricSql = ", ".join(map(lambda x: f"{x} double precision", self.metrics))
            sql = f"CREATE TABLE {t} (ilcapo integer NOT NULL, name character varying NOT NULL, yearmonth character(7) NOT NULL, {metricSql}, PRIMARY KEY (ilcapo, name, yearmonth) );"
            cur.execute(sql)
            self.__connection.commit()
            

            self.buffer[t] = []
        cur.close()

    def dropTables(self, tables):
        cur = self.__connection.cursor()
        for t in tables:
            cur.execute(f"DROP TABLE IF EXISTS {t}")
            self.__connection.commit()
        cur.close()

    def insertMetrics(self, lang: str, ilcapo: int, name: str, yearmonth: str, metrics: List[Tuple[float, float, float, float]]) -> None:
        params = [ilcapo, name, yearmonth] + self.__flatList__(metrics)

        self.buffer[lang].append(params)
        self.bufferLen += 1

        if (self.bufferLen > 10000):
            print("Inserting bufferone")
            self.insertBuffer()

    def finalize(self):
        self.insertBuffer()

    def insertBuffer(self):
        cur = self.__connection.cursor()
        for table in self.buffer:
            if (len(self.buffer[table]) > 0):
                psycopg2.extras.execute_batch(cur, f"INSERT INTO {table} {self.insertSqlNames}", self.buffer[table])
                self.__connection.commit()
                self.buffer[table] = []
        cur.close()
        self.bufferLen = 0