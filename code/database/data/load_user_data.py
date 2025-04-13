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
        ("Alice", "Durand", "alice@example.com", 30, "Scientist"),
        ("Bob", "Martin", "bob@example.com", 28, "Passionate"),
        ("Charlie", "Lemoine", "charlie@example.com", 35, "Scientist"),
        ("Diane", "Berger", "diane@example.com", 40, "Passionate"),
        ("Eve", "Dupont", "eve@example.com", 25, "Scientist"),
        ("François", "Moreau", "francois@example.com", 27, "Passionate"),
        ("Gabrielle", "Leroy", "gabrielle@example.com", 33, "Scientist"),
        ("Hugo", "Lefevre", "hugo@example.com", 29, "Passionate"),
        ("Isabelle", "Girard", "isabelle@example.com", 32, "Scientist"),
        ("Julien", "Renard", "julien@example.com", 26, "Passionate")
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
