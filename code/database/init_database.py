import pymysql.cursors
import load_all_data
from models.database import get_db_connection


connection = get_db_connection()


cursor = connection.cursor()

cursor.execute("DROP DATABASE IF EXISTS glo_2005_projet;")

cursor.execute("CREATE DATABASE IF NOT EXISTS glo_2005_projet;")

cursor.execute("USE glo_2005_projet;")

create_tables = [
    """
CREATE TABLE IF NOT EXISTS User (
    uid INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    password_hash VARCHAR(255) NOT NULL DEFAULT '',
    user_type ENUM('Scientist', 'Passionate') NOT NULL,
    account_creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    observation_count INT DEFAULT 0,
    PRIMARY KEY (uid)
);

    """,
"""
    CREATE TABLE IF NOT EXISTS Species (
        latin_name VARCHAR(100) NOT NULL,
        name VARCHAR(100),
        genus VARCHAR(100),
        family VARCHAR(100),
        order_name VARCHAR(100),
        class_name VARCHAR(100),
        phylum VARCHAR(100),
        kingdom ENUM('Plant', 'Algae', 'Fungus', 'Animal'),
        description VARCHAR(500),
        PRIMARY KEY(latin_name)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Place (
    pid INT NOT NULL AUTO_INCREMENT, 
    name VARCHAR(100),                      
    latitude DOUBLE NOT NULL CHECK (latitude BETWEEN -90 AND 90), 
    longitude DOUBLE NOT NULL CHECK (longitude BETWEEN -180 AND 180),  
    PRIMARY KEY (pid) 
);
    """,
    """
    CREATE TABLE ClimateRegion (
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    climate VARCHAR(200),
    koppen_geiger_zone VARCHAR(10),
    PRIMARY KEY(latitude, longitude)

);

    """,
     """
    CREATE TABLE IF NOT EXISTS Photo (
    photo_id INT NOT NULL AUTO_INCREMENT,
    image_data MEDIUMBLOB NOT NULL,
    PRIMARY KEY(photo_id)
    );
    """
    ,
    """
   CREATE TABLE IF NOT EXISTS Observation (
    oid INT NOT NULL AUTO_INCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    author_uid INT NOT NULL,
    species VARCHAR(100) NOT NULL,
    behavior ENUM('Sleeping', 'Eating', 'Hunting', 'Moving', 'Interacting') NOT NULL,
    description VARCHAR(500),
    pid INT NOT NULL,
    photo_id INT NOT NULL,
    rating INT DEFAULT NULL,  
    PRIMARY KEY (oid),
    FOREIGN KEY (author_uid) REFERENCES User(uid),
    FOREIGN KEY (species) REFERENCES Species(latin_name),
    FOREIGN KEY (pid) REFERENCES Place(pid),
    FOREIGN KEY (photo_id) REFERENCES Photo(photo_id)
);

    """,
    """
    CREATE TABLE IF NOT EXISTS Comment (
        cid INT AUTO_INCREMENT NOT NULL,
        text VARCHAR(300),
        observation_oid INT,
        commenter_uid INT,
        PRIMARY KEY(cid),
        FOREIGN KEY(observation_oid) REFERENCES Observation(oid),
        FOREIGN KEY(commenter_uid) REFERENCES User(uid)
    );
    """,

    """
    CREATE TABLE IF NOT EXISTS Note(
        nid INT NOT NULL,
        observation_oid INT NOT NULL,
        user_uid INT NOT NULL,
        rating INT CHECK (rating BETWEEN 0 AND 5),
        PRIMARY KEY(nid),
        FOREIGN KEY(observation_oid) REFERENCES Observation(oid),
        FOREIGN KEY(user_uid) REFERENCES User(uid)
    );
    """
]


for query in create_tables:
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Error :\n{query}\nErreur: {e}")
        exit(1)

triggers_sql =[ """
    CREATE TRIGGER IF NOT EXISTS after_note_insert AFTER INSERT ON Note
    FOR EACH ROW
    BEGIN
    DECLARE avg_rating FLOAT;
    SELECT AVG(N.rating) INTO avg_rating
    FROM Note N WHERE observation_oid = NEW.observation_oid;

    UPDATE Observation
    SET rating = avg_rating WHERE oid = NEW.observation_oid;
    END;
    """
    ,   
    """
    CREATE TRIGGER IF NOT EXISTS observation_count_update_insert
    AFTER INSERT ON Observation
    FOR EACH ROW
    BEGIN
    UPDATE User
    SET observation_count = observation_count + 1
    WHERE uid = NEW.author_uid;
    END;
    """
,
    """
    CREATE TRIGGER IF NOT EXISTS observation_count_update_delete
    AFTER DELETE ON Observation
    FOR EACH ROW
    BEGIN
    UPDATE User
    SET observation_count = observation_count - 1
    WHERE uid = OLD.author_uid;
    END;
    """
,

    """
    CREATE TRIGGER IF NOT EXISTS filter_language_comment_insert BEFORE INSERT ON Comment
    FOR EACH ROW
    BEGIN
    IF LOWER(NEW.text) LIKE '%%fuck%%' THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Profanity is not allowed in comments.';
    END IF;
    END;
    """
    ,
    """
    CREATE TRIGGER IF NOT EXISTS filter_language_update BEFORE UPDATE ON Comment
    FOR EACH ROW
    BEGIN
    IF LOWER(NEW.text) LIKE '%%fuck%%' THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Profanity is not allowed in comments.';
    END IF;
    END;
    """
]
for trigger in triggers_sql:
    try:
        cursor.execute(trigger)
        connection.commit()

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

index_sql = [
    """
    CREATE INDEX user_name ON User(first_name, last_name);
    """
    ,
    """
    CREATE INDEX observed_species ON Observation(species);
    """
]

for index in index_sql:
    try:
        cursor.execute(index)
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")

print("All BD created")

load_all_data.main()

print("load data called")

cursor.close()
connection.close()
