import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from models.database import get_db_connection

def load_places():
    connection = get_db_connection()
    cursor = connection.cursor()

    places = [
        ("Parc National de la Mauricie", 46.8000, -73.1000),
        ("Mont-Tremblant", 46.1186, -74.5961),
        ("Parc des Grands-Jardins", 47.6667, -70.6667),
        ("Lac Saint-Jean", 48.4333, -71.2333),
        ("Forêt Montmorency", 47.3300, -71.1500),
        ("Gaspé", 48.8333, -64.4833),
        ("Baie-Comeau", 49.2167, -68.1500),
        ("Rimouski", 48.4500, -68.5333),
        ("Val-d’Or", 48.1000, -77.7833),
        ("Île d’Orléans", 46.9000, -71.0167)
    ]

    query = """
        INSERT INTO Place (name, latitude, longitude) 
        VALUES (%s, %s, %s)
    """

    try:
        cursor.executemany(query, places)
        connection.commit()
        print("places added successfully!")
    except Exception as e:
        print(f"Error inserting places: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    load_places()


