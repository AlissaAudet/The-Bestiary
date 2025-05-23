import pymysql
import requests
from models.database import get_db_connection

def get_place_by_coordinates(latitude, longitude, place_name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT pid FROM Place 
                WHERE name = %s AND latitude = %s AND longitude = %s
            """, (place_name, latitude, longitude))
            result = cursor.fetchone()

            if result and isinstance(result, tuple):
                return result[0]
            return None

    except pymysql.MySQLError as e:
        print(f" Database error in get_place_by_coordinates(): {e}")
        return None

    finally:
        connection.close()


def insert_place(place_name, latitude, longitude):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT pid FROM Place 
            WHERE name = %s AND latitude = %s AND longitude = %s
        """, (place_name, latitude, longitude))
        result = cursor.fetchone()

        if result:
            return result[0]
        cursor.execute("""
            INSERT INTO Place (name, latitude, longitude)
            VALUES (%s, %s, %s)
        """, (place_name, latitude, longitude))
        connection.commit()
        pid = cursor.lastrowid
        cursor.execute("""
            SELECT * FROM ClimateRegion 
            WHERE latitude = %s AND longitude = %s
        """, (latitude, longitude))
        existing_climate = cursor.fetchone()

        if not existing_climate:
            climate = None
            koppen_geiger_zone = None
            try:
                climate_url = f"http://climateapi.scottpinkelman.com/api/v1/location/{latitude}/{longitude}"
                response = requests.get(climate_url)
                if response.status_code == 200:
                    data = response.json()
                    values = data.get("return_values", [])
                    if values:
                        climate = values[0].get("zone_description")
                        koppen_geiger_zone = values[0].get("koppen_geiger_zone")
                else:
                    print(f"Error fetching climate data: HTTP {response.status_code}")
            except Exception as e:
                print(f"Climate API error: {e}")

            cursor.execute("""
                INSERT INTO ClimateRegion (latitude, longitude, climate, koppen_geiger_zone)
                VALUES (%s, %s, %s, %s)
            """, (latitude, longitude, climate, koppen_geiger_zone))
            connection.commit()

        return pid

    except pymysql.MySQLError as e:
        print("Database error in insert_place:", e)
        connection.rollback()
        return None

    except Exception as e:
        print("General error in insert_place:", e)
        connection.rollback()
        return None

    finally:
        cursor.close()
        connection.close()


def get_places():
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT pid, name, latitude, longitude FROM Place")
        places = cursor.fetchall()
        return places if places else []

    except pymysql.MySQLError as e:
        print(f"Database error in get_places(): {e}")
        return []

    finally:
        cursor.close()
        connection.close()
