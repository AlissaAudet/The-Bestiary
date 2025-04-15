import pymysql.cursors
import load_all_data
from models.database import get_db_connection

from database_setup.table import create_tables
from database_setup.trigger import create_triggers
from database_setup.index import create_indexs
from database_setup.function import create_functions

connection = get_db_connection()

cursor = connection.cursor()

#cursor.execute("DROP DATABASE IF EXISTS glo_2005_projet;")

#cursor.execute("CREATE DATABASE IF NOT EXISTS glo_2005_projet;")

cursor.execute("USE glo_2005_projet;")

def execute_queries(title, queries):
    for query in queries:
        try:
            cursor.execute(query)
            connection.commit()
        except pymysql.MySQLError as e:
            print(f"[{title}] Error: {e}\nQuery:\n{query}\n")


execute_queries("TABLE", create_tables)
execute_queries("FUNCTION", create_functions)
execute_queries("TRIGGER", create_triggers)
execute_queries("INDEX", create_indexs)

print("All BD created")

#load_all_data.main()

print("All data created")

cursor.close()
connection.close()
