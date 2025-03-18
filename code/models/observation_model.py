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





