import sys
import os
#
#doit etre modif pour avoir les clé comme attibut


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from models.database import get_db_connection


def load_users():
    connection = get_db_connection()
    cursor = connection.cursor()

    users = [
        ("a",	"a",	"a",	1,	"$2b$12$BaFgZ.WTVjy34VoFB3IMDeZ4cU4n60oi7gVCg5i1le02B2HvHQDcy")
    ]

    query = """
        INSERT INTO User (first_name, last_name, email, age, password_hash) 
        VALUES (%s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(query, users)
        connection.commit()
        print("users added successfully!")
    except Exception as e:
        print(f"Error inserting users: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    load_users()
