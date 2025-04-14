import pymysql
from models.database import get_db_connection

def follow_user(follower_uid, following_uid):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT IGNORE INTO Followers (follower_uid, following_uid)
                VALUES (%s, %s)
            """, (follower_uid, following_uid))
            connection.commit()
            return True
    except pymysql.MySQLError as e:
        print(f"Database error in follow_user: {e}")
        return False
    finally:
        connection.close()

def unfollow_user(follower_uid, following_uid):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM Followers
                WHERE follower_uid = %s AND following_uid = %s
            """, (follower_uid, following_uid))
            connection.commit()
            return True
    except pymysql.MySQLError as e:
        print(f"Database error in unfollow_user: {e}")
        return False
    finally:
        connection.close()


def get_followers(uid):
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT u.uid, u.first_name, u.last_name
                FROM Followers f
                JOIN User u ON f.follower_uid = u.uid
                WHERE f.following_uid = %s
            """, (uid,))
            return cursor.fetchall()
    finally:
        connection.close()


def get_following(uid):
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT u.uid, u.first_name, u.last_name
                FROM Followers f
                JOIN User u ON f.following_uid = u.uid
                WHERE f.follower_uid = %s
            """, (uid,))
            return cursor.fetchall()
    finally:
        connection.close()


def is_following_user(follower_uid, following_uid):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1 FROM Followers
                WHERE follower_uid = %s AND following_uid = %s
                LIMIT 1
            """, (follower_uid, following_uid))
            return cursor.fetchone() is not None
    except pymysql.MySQLError as e:
        print(f"Database error in is_following_user: {e}")
        return False
    finally:
        connection.close()
