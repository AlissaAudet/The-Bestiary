import pymysql
from models.database import get_db_connection


def insert_photo(image_data):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Photo (image_data) VALUES (%s)
                """, image_data
            )
            connection.commit()
            photo_id = cursor.lastrowid

            return photo_id


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