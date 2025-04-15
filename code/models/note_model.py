from models.database import get_db_connection

def insert_or_update_note(nid, observation_oid, user_uid, rating):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        check_query = """
            SELECT nid FROM Note
            WHERE observation_oid = %s AND user_uid = %s
        """
        cursor.execute(check_query, (observation_oid, user_uid))
        existing = cursor.fetchone()

        if existing:
            update_query = """
                UPDATE Note
                SET rating = %s
                WHERE observation_oid = %s AND user_uid = %s
            """
            cursor.execute(update_query, (rating, observation_oid, user_uid))
        else:
            insert_query = """
                INSERT INTO Note (nid, observation_oid, user_uid, rating)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (nid, observation_oid, user_uid, rating))

        connection.commit()
        return True
    except Exception as e:
        print(f"Error in insert_or_update_note: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def get_user_rating_for_observation(user_id, observation_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT rating
            FROM Note
            WHERE user_uid = %s AND observation_oid = %s
            LIMIT 1
        """
        cursor.execute(query, (user_id, observation_id))
        result = cursor.fetchone()
        return result['rating'] if result else None
    finally:
        cursor.close()
        connection.close()
