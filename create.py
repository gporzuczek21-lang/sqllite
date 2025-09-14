import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except Error as e:
       print(e)
   return conn

def execute_sql(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)
       
def add_przepis(conn, przepis):
   """
   Create a new przepis into the przepisy table
   :param conn:
   :param przepis:
   :return: przepis id
   """
   sql = '''INSERT INTO przepisy(nazwa, czas)
             VALUES(?,?)'''
   cur = conn.cursor()
   cur.execute(sql, przepis)
   conn.commit()
   return cur.lastrowid 

def add_skladnik(conn,skladnik):
   """
   Create a new skladnik into the skladniki table
   :param conn:
   :param skladnik:
   :return: skladnik id
   """
   sql = '''INSERT INTO skladniki(przepis_id, nazwa, ilosc, miara)
             VALUES(?,?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, skladnik)
   conn.commit()
   return cur.lastrowid

if __name__ == "__main__":

   create_przepisy_sql = """
   -- przepisy table
   CREATE TABLE IF NOT EXISTS przepisy (
      id integer PRIMARY KEY,
      nazwa text NOT NULL,
      czas text
   );
   """
   create_skladniki_sql = """
   -- skladniki table
   CREATE TABLE IF NOT EXISTS skladniki (
      id integer PRIMARY KEY,
      przepis_id integer NOT NULL,
      nazwa text NOT NULL,
      ilosc text NOt NULL,
      miara text NOT NULL,
      FOREIGN KEY (przepis_id) REFERENCES przepisy (id)
   );
   """
 
   db_file = "database.db"

   conn = create_connection(db_file)
   if conn is not None:
       execute_sql(conn, create_przepisy_sql)
       execute_sql(conn, create_skladniki_sql)
       conn.close()

   conn = create_connection("database.db")
   przepis = ("jajecznica", "10 minut")
   pr_id = add_przepis(conn, przepis)

   skladnik =(pr_id,"jajko","2","szt")
   skladnik_id=add_skladnik(conn, skladnik)
   skladnik =(pr_id,"maslo","5","g")
   skladnik_id=add_skladnik(conn, skladnik)
   skladnik =(pr_id,"szczypiorek","1","garsc")
   skladnik_id=add_skladnik(conn, skladnik)

   przepis = ("grzanka","5 minut")
   pr_id = add_przepis(conn, przepis)
   skladnik =(pr_id,"chleb","2","kromki")
   skladnik_id=add_skladnik(conn, skladnik)
   skladnik =(pr_id,"ser","2","plastrki")
   skladnik_id=add_skladnik(conn, skladnik)
   skladnik =(pr_id,"szynka","1","plaster")
   skladnik_id=add_skladnik(conn, skladnik)
   print(pr_id,skladnik_id)

   conn.commit()
   conn.close()
