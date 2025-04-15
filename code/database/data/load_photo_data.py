import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from models.database import get_db_connection

def load_photos_from_directory(directory_path):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        for filename in os.listdir(directory_path):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                full_path = os.path.join(directory_path, filename)
                with open(full_path, "rb") as image_file:
                    binary_data = image_file.read()
                    cursor.execute("INSERT INTO Photo (image_data) VALUES (%s)", (binary_data,))

        connection.commit()
        print("All photos inserted successfully!")

    except Exception as e:
        print(f"Error inserting photo: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    image_folder_path = os.path.join(os.path.dirname(__file__), "image"
                                                                "")
    load_photos_from_directory(image_folder_path)
