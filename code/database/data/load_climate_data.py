import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from models.database import get_db_connection

def load_climate_region():
    connection = get_db_connection()
    cursor = connection.cursor()

    climate_data = [
        (
            46.0,
            -71.0,
            "Humid continental, no dry season, warm summer",
            "Dfb"
        )
    ]

    query = """
        INSERT INTO ClimateRegion (latitude, longitude, climate, koppen_geiger_zone)
        VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.executemany(query, climate_data)
        connection.commit()
        print("Climate region inserted successfully!")
    except Exception as e:
        print(f"Error inserting climate region: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    load_climate_region()
