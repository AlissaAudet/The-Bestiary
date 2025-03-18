from models.database import get_db_connection

def get_species():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT latin_name AS id, name FROM Species")
    species = cursor.fetchall()

    cursor.close()
    connection.close()
    return species