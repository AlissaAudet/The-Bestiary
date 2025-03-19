import pymysql
from models.database import get_db_connection

def get_species():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT latin_name AS id, name FROM Species")
    species = cursor.fetchall()

    cursor.close()
    connection.close()
    return species

def search_species(query):
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    query = f"%{query.replace(' ', '')}%"

    sql = """
        SELECT latin_name AS id, name 
        FROM Species
        WHERE REPLACE(name, ' ', '') LIKE %s 
        OR REPLACE(latin_name, ' ', '') LIKE %s
    """

    cursor.execute(sql, (query, query))
    species = cursor.fetchall()

    cursor.close()
    connection.close()
    return species