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
        ("Stephanie",	"Tremblay",	"stephanie@gmail.com",	20,	"$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe"),
        ("Martine", "Leclerc", "martine@gmail.com", 40, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe")
    ]

    query = """
        INSERT INTO User (first_name, last_name, email, age, user_type) 
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
