import pymysql
from models.database import get_db_connection

def get_species():
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        query = "SELECT latin_name AS id, name FROM Species"
        cursor.execute(query)
        species = cursor.fetchall()

        return species if species else []

    except pymysql.MySQLError as e:
        print(f" Database error in get_species(): {e}")
        return []

    finally:
        cursor.close()
        connection.close()

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