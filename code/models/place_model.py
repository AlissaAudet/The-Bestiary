from models.database import get_db_connection

def get_places():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT pid AS id, name FROM Place")
    places = cursor.fetchall()

    cursor.close()
    connection.close()
    return places

def get_place_by_coordinates(latitude, longitude, name):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        name = name.strip()

        print(f"🛠 Running SQL: SELECT pid FROM Place WHERE latitude = {latitude} AND longitude = {longitude} AND name = '{name}'")

        query = """
            SELECT pid FROM Place 
            WHERE ROUND(latitude, 6) = ROUND(%s, 6) 
            AND ROUND(longitude, 6) = ROUND(%s, 6) 
            AND TRIM(name) COLLATE utf8mb4_general_ci = TRIM(%s)
        """
        cursor.execute(query, (float(latitude), float(longitude), name))

    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def insert_place(name, latitude, longitude, admin_region=None, climate=None):

    latitude = float(latitude)
    longitude = float(longitude)
    name = str(name).strip()

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        existing_place = get_place_by_coordinates(latitude, longitude, name)
        if existing_place:
            print(f"Place already exists with pid: {existing_place['pid']}")
            return existing_place['pid']

        query_insert = """
            INSERT INTO Place (name, latitude, longitude, admin_region, climate)
            VALUES (%s, %s, %s, %s, %s)
        """
        print(f"Running SQL INSERT: {query_insert} → ({name}, {latitude}, {longitude}, {admin_region}, {climate})")
        cursor.execute(query_insert, (name, latitude, longitude, admin_region, climate))
        connection.commit()

        return cursor.lastrowid

    except Exception as e:
        print(f"Database error inserting place: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


