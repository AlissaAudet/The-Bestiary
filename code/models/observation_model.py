import pymysql
from models.database import get_db_connection

def insert_observation(user_id, species, timestamp, behavior, description, pid):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Observation (author_uid, species, timestamp, behavior, description, pid)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(query, (user_id, species, timestamp, behavior, description, pid))
        connection.commit()
        print(f"Observation added (User {user_id} - Species {species} at {timestamp})")
        return True
    except Exception as e:
        print(f"Database error inserting observation: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def fetch_observations_by_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        query = """
            SELECT oid, timestamp, species, description, pid
            FROM Observation
            WHERE author_uid = %s
            ORDER BY timestamp DESC;
        """
        cursor.execute(query, (user_id,))
        observations = cursor.fetchall()

        return observations

    except pymysql.MySQLError as e:
        print(f"Database error in fetch_observations_by_user(): {e}")
        return []

    finally:
        cursor.close()
        connection.close()




