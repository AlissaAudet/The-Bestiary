import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        db="glo_2005_projet",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )

