import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from models.database import get_db_connection

def load_forbidden_words(file_path, max_words=1000):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            unique_words = set(word.strip().lower() for word in lines if word.strip())

        selected_words = list(unique_words)[:max_words]
        word_data = [(word,) for word in selected_words]

        query = "INSERT INTO ForbiddenWords (word) VALUES (%s)"

        cursor.executemany(query, word_data)
        connection.commit()
        print(f"{len(word_data)} forbidden words inserted successfully!")

    except Exception as e:
        print(f"Error inserting forbidden words: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    words_path = os.path.join(os.path.dirname(__file__), "txt", "english_bad_words.txt")
    load_forbidden_words(words_path)
