import pymysql.cursors
import load_all_data


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    autocommit=True
)

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
    password_hash VARCHAR(255) NOT NULL,
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
    """,
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
        cid INT NOT NULL,
        text VARCHAR(300),
        observation_oid INT,
        PRIMARY KEY(cid),
        FOREIGN KEY(observation_oid) REFERENCES Observation(oid)
    );
    """
]

create_index = [
    """
    CREATE INDEX idx_user_first_name ON User(first_name);
    """,
    """
    CREATE INDEX idx_observation_species ON Observation(species);
    """,
    """
    CREATE INDEX idx_place_lat_long ON Place(latitude, longitude);
    """

]

for query in create_tables:
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Error :\n{query}\nErreur: {e}")
        exit(1)

for index_query in create_index:
    try:
        cursor.execute(index_query)
    except Exception as e:
        print(f" Error:\n{index_query}\nErreur: {e}")


print("All BD created")

load_all_data.main()

print("load data called")

cursor.close()
connection.close()
