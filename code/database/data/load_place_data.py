import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from models.database import get_db_connection

def load_places():
    connection = get_db_connection()
    cursor = connection.cursor()

    places = [

        ("Parc National de la Mauricie", 46.0, -71.0),
        ("Mont-Tremblant", 46.0, -71.0),
        ("Parc des Grands-Jardins", 46.0, -71.0),
        ("Lac Saint-Jean", 46.0, -71.0),
        ("Forêt Montmorency", 46.0, -71.0),
        ("Gaspé", 46.0, -71.0),
        ("Baie-Comeau", 46.0, -71.0),
        ("Rimouski", 46.0, -71.0),
        ("Val-d’Or", 46.0, -71.0),
        ("Île d’Orléans", 46.0, -71.0)
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


