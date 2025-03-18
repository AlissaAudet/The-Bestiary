from models.database import get_db_connection

def get_users():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT uid AS id, CONCAT(first_name, ' ', last_name) AS name FROM User")
    users = cursor.fetchall()

    cursor.close()
    connection.close()
    return users

def insert_user(first_name, last_name, age, user_type):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO User (first_name, last_name, email, age, user_type) 
        VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(query, (first_name, last_name, email, age, user_type))
        connection.commit()
    except Exception as e:
        print(f"Erreur SQL : {e}")
    finally:
        cursor.close()
        connection.close()
