import pymysql
from models.database import get_db_connection

def insert_note(nid, observation_oid, user_uid, note):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Note (nid, observation_oid, user_uid, note)
        VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (nid, observation_oid, user_uid, note))
        connection.commit()
        print(f"Rating submitted!")
        return True
    except Exception as e:
        print(f"Database error inserting rating: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

