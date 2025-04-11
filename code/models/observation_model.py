import pymysql
from models.database import get_db_connection
from models.place_model import get_place_by_coordinates


def insert_observation(user_id, species, timestamp, behavior, description, pid, photo_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Observation (author_uid, species, timestamp, behavior, description, pid, photo_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    try:

        cursor.execute(query, (user_id, species, timestamp, behavior, description, pid, photo_id))
        connection.commit()
        return True

    except Exception as e:
        print("ERROR:", e)
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()


def fetch_observations_by_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        query = """
            SELECT oid, timestamp, species, description, pid
            FROM Observation
            WHERE author_uid = %s
            ORDER BY timestamp DESC;
        """
        cursor.execute(query, (user_id,))
        observations = cursor.fetchall()

        return observations

    except pymysql.MySQLError as e:
        print(f"Database error in fetch_observations_by_user(): {e}")
        return []

    finally:
        cursor.close()
        connection.close()


def fetch_observations_by_user(uid):
    connection = get_db_connection()
    observations = []

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT oid, timestamp, description, species
                FROM Observation
                WHERE author_uid = %s
                ORDER BY timestamp DESC
            """
            cursor.execute(sql, (uid,))
            observations = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching observations for user {uid}: {e}")
    finally:
        connection.close()

    return observations



def fetch_observation_by_id(oid):
    connection = get_db_connection()
    observation = None

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT o.oid, o.timestamp, o.description, o.behavior, s.name AS species_name, s.latin_name AS species, u.first_name, u.last_name, u.uid, f.image_data, p.name AS place_name, p.latitude, p.longitude, p.admin_region, p.climate
                FROM Observation o
                JOIN Species s ON o.species = s.latin_name
                JOIN User u ON o.author_uid = u.uid
                JOIN Photo f on o.photo_id = f.photo_id
                JOIN Place p on o.pid = p.pid
                WHERE o.oid = %s
            """
            cursor.execute(sql, (oid,))
            observation = cursor.fetchone()
    except Exception as e:
        print(f"Error fetching observation {oid}: {e}")
    finally:
        connection.close()

    return observation


def fetch_filtered_observations(author=None, species=None, behavior=None, timestamp=None, place_name=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT *
        FROM Observation o
        JOIN User u ON o.author_uid = u.uid
        JOIN Species s ON o.species = s.latin_name
		JOIN Place p ON o.pid = p.pid
        WHERE 1=1
    """

    params = []

    if author != "":
        query += " AND CONCAT(u.first_name, ' ', u.last_name) = %s"
        params.append(author)

    if species:
        query += " AND o.species = %s"
        params.append(species)

    if behavior:
        query += " AND o.behavior = %s"
        params.append(behavior)

    if timestamp:
        query += " AND o.timestamp = %s"
        params.append(timestamp)

    if place_name:
        query += " AND p.name = %s"
        params.append(place_name)


    print("SQL Query:", query)
    print("Parameters:", params)

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    observations = []

    for obs in results:
        observation = {
            "oid": obs["oid"],
            "author": obs["first_name"] + " " + obs["last_name"],
            "species": obs["species"],
            "behavior": obs["behavior"],
            "timestamp": obs["timestamp"],
            "place_name": obs["p.name"],
        }
        observations.append(observation)

    return observations


# observation_model.py

import pymysql
from models.database import get_db_connection


def insert_comment(user_id, observation_id, comment_text):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO Comment (text, observation_oid, commenter_uid)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(query, (comment_text, observation_id, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error inserting comment: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def fetch_comments_by_observation_id(observation_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT Comment.cid, Comment.text, User.first_name, User.last_name
        FROM Comment
        JOIN User ON Comment.commenter_uid = User.uid
        WHERE Comment.observation_oid = %s
        ORDER BY cid
    """
    cursor.execute(query, (observation_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()

    return comments
