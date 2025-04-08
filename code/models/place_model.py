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
            pid = result[0]
        else:
            cursor.execute("""
                INSERT INTO Place (name, latitude, longitude) 
                VALUES (%s, %s, %s)
            """, (place_name, latitude, longitude))
            connection.commit()
            pid = cursor.lastrowid

        return pid

    except pymysql.MySQLError as e:
        print("Database error in insert_place_with_climate:", e)
        connection.rollback()
        return None

    except Exception as e:
        print("General error in insert_place_with_climate:", e)
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
