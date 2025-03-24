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



def fetch_observations_by_user(uid):
    connection = get_db_connection()
    observations = []

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT oid, timestamp, description, species
                FROM Observation
                WHERE author_uid = %s
                ORDER BY timestamp DESC
            """
            cursor.execute(sql, (uid,))
            observations = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching observations for user {uid}: {e}")
    finally:
        connection.close()

    return observations



def fetch_observation_by_id(oid):
    connection = get_db_connection()
    observation = None

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                 SELECT o.oid, o.timestamp, o.description, s.latin_name AS species, u.first_name, u.last_name, u.uid
                FROM Observation o
                JOIN Species s ON o.species = s.latin_name
                JOIN User u ON o.author_uid = u.uid
                WHERE o.oid = %s
            """
            cursor.execute(sql, (oid,))
            observation = cursor.fetchone()
    except Exception as e:
        print(f"Error fetching observation {oid}: {e}")
    finally:
        connection.close()

    return observation