import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from models.database import get_db_connection

def load_observations():
    connection = get_db_connection()
    cursor = connection.cursor()

    observations = [
        # User 1 (stephanie)
        ("2024-04-01 10:00:00", 1, "Odocoileus virginianus", "Interacting", "near the lake", 1, 1),
        ("2023-08-01 10:00:00", 1, "Bubo scandiacus", "Hunting", "was hunting", 2, 2),
        ("2023-10-01 10:00:00", 1, "Marmota monax", "Interacting", "Defended its territory", 3, 3),
        # User 2 (martine)
        ("2024-06-01 10:00:00", 2, "Anaxyrus americanus", "Moving", "3 inches long", 4, 4),
        ("2024-08-01 10:00:00", 2, "Ardea alba", "Hunting", "", 5, 5),
        ("2025-03-01 10:00:00", 2, "Sciurus carolinensis", "Eating", "Cold Day", 6,6)
    ]

    try:
        cursor.executemany("""
            INSERT INTO Observation (
                timestamp, author_uid, species, behavior, description, pid, photo_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, observations)
        connection.commit()
        print("observations inserted successfully.")
    except Exception as e:
        print(f"Error inserting observations: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    load_observations()
