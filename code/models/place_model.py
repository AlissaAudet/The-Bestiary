from models.database import get_db_connection

def get_place_by_coordinates(latitude, longitude, place_name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT pid FROM Place 
                WHERE name = %s AND latitude = %s AND longitude = %s
            """, (place_name, latitude, longitude))
            return cursor.fetchone()
    finally:
        connection.close()

def insert_place(place_name, latitude, longitude):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Place (name, latitude, longitude) 
                VALUES (%s, %s, %s)
            """, (place_name, latitude, longitude))
        connection.commit()
    finally:
        connection.close()

def get_places():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Place")
            return cursor.fetchall()
    finally:
        connection.close()