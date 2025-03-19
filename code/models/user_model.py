import pymysql
from models.database import get_db_connection

def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT uid, first_name, last_name FROM User")
        users = cursor.fetchall()
        return users
    except Exception as e:
        print(f"Database error fetching users: {e}")
        return []
    finally:
        cursor.close()
        connection.close()


def search_users(query):
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    query = f"%{query}%"
    sql = """
        SELECT uid AS id, CONCAT(first_name, ' ', last_name) AS name
        FROM User
        WHERE first_name LIKE %s 
        OR last_name LIKE %s
        OR CONCAT(first_name, ' ', last_name) LIKE %s
    """
    cursor.execute(sql, (query, query, query))
    users = cursor.fetchall()

    cursor.close()
    connection.close()
    return users



def get_user_by_id(uid):
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        query ="""
            SELECT uid, first_name, last_name, email, age, user_type, 
                   account_creation_date, observation_count
            FROM User
            WHERE uid = %s;
            """
        cursor.execute(query, (uid,))
        user = cursor.fetchone()
        return user if user else None

    except Exception as e:
        print(f"Database error fetching user by ID: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def insert_user(first_name, last_name, email, age, user_type):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO User (first_name, last_name, email, age, user_type)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, email, age, user_type))

        connection.commit()
        print(f" User inserted: {first_name} {last_name} (email: {email})")

    except Exception as e:
        print(f" Error inserting user: {e}")

    finally:
        cursor.close()
        connection.close()

