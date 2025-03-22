import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from models.database import get_db_connection

def load_places():
    connection = get_db_connection()
    cursor = connection.cursor()

    places = [
        ("Parc national de la Gaspésie", 48.9455, -66.3986, "Gaspésie–Îles-de-la-Madeleine", "Boreal"),
        ("Mont Tremblant", 46.1181, -74.5962, "Laurentides", "Humid Continental"),
        ("Parc national de la Jacques-Cartier", 47.1655, -71.2927, "Capitale-Nationale", "Subarctic")
    ]

    query = """
        INSERT INTO Place (name, latitude, longitude, admin_region, climate) 
        VALUES (%s, %s, %s, %s, %s)
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


