import os
import sys
import random
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from models.database import get_db_connection


def generate_random_observation(uid_range=(1, 17), pid_range=(1, 10), photo_id=7):
    species_list = [
        "Odocoileus virginianus","Marmota monax"
    ]
    behaviors = ["Sleeping", "Eating", "Hunting", "Moving", "Interacting"]
    descriptions = [
        "Observed near a river", "Eating berries", "Sleeping in a tree",
        "Interacting with others", "Crossing the path", "Running away",
        "Resting quietly", "Displaying dominance"
    ]

    timestamp = datetime.now() - timedelta(days=random.randint(0, 1000))
    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    return (
        formatted_time,
        random.randint(*uid_range),
        random.choice(species_list),
        random.choice(behaviors),
        random.choice(descriptions),
        random.randint(*pid_range),
        photo_id
    )

def load_random_observations(n):
    connection = get_db_connection()
    cursor = connection.cursor()

    observations = [generate_random_observation() for _ in range(n)]

    query = """
        INSERT INTO Observation (
            timestamp, author_uid, species, behavior, description, pid, photo_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(query, observations)
        connection.commit()
        print(f"{n} random observations inserted successfully.")
    except Exception as e:
        print(f"Error inserting random observations: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

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
    load_random_observations(100)
