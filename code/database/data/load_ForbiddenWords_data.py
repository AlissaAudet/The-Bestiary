import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from models.database import get_db_connection

def load_forbidden_words():
    connection = get_db_connection()
    cursor = connection.cursor()

    word_data = [
        ("calice"),
        ("câlice"),
        ("ciboire"),
        ("câline"),
        ("crisse"),
        ("esti"),
        ("hostie"),
        ("ostie"),
        ("tabarnak"),
        ("tabarnacle"),
        ("sacrament"),
        ("maudit"),
        ("batinse"),
        ("batèche"),
        ("calvaire"),
        ("torvisse"),
        ("mosus"),
        ("cibolac"),
        ("cibouleau"),
        ("baptême"),
        ("câlisse"),
        ("enweye donc"),
        ("christie"),
        ("sacristie"),
        ("sacréfice"),
        ("marde"),
        ("fuck")
    ]

    query = """
        INSERT INTO ForbiddenWords (word)
        VALUES (%s)
    """

    try:
        cursor.executemany(query, word_data)
        connection.commit()
        print("Forbidden words inserted successfully!")
    except Exception as e:
        print(f"Error inserting Forbidden words: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    load_forbidden_words()
