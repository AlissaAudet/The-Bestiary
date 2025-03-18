import pymysql.cursors

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    autocommit=True
)

cursor = connection.cursor()

#Supprime toutes les tables pour reinitialise
cursor.execute("DROP DATABASE IF EXISTS glo_2005_projet;")

cursor.execute("CREATE DATABASE IF NOT EXISTS glo_2005_projet;")

cursor.execute("USE glo_2005_projet;")

create_tables = [
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
        description VARCHAR(300),
        PRIMARY KEY(latin_name)
    );
    """,
    """
CREATE TABLE IF NOT EXISTS User (
    uid INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    user_type ENUM('Scientist', 'Passionate') NOT NULL,
    account_creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    observation_count INT DEFAULT 0,
    PRIMARY KEY (uid)
);

    """
    ,
    """
    CREATE TABLE IF NOT EXISTS Place (
        latitude DOUBLE NOT NULL,
        longitude DOUBLE NOT NULL,
        admin_region ENUM('Abitibi-Témiscamingue', 'Bas-Saint-Laurent', 'Capitale-Nationale', 'Centre-du-Québec', 'Chaudière-Appalaches',
                          'Côte-Nord', 'Estrie', 'Gaspésie–Îles-de-la-Madeleine', 'Lanaudière', 'Laurentides', 'Laval', 'Mauricie',
                          'Montérégie', 'Nord-du-Québec', 'Outaouais', 'Saguenay–Lac-Saint-Jean'),
        mrc VARCHAR(50),
        climate ENUM('Humid Continental', 'Subarctic', 'Arctic'),
        PRIMARY KEY(latitude, longitude)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Observation (
        oid INT NOT NULL,
        timestamp TIMESTAMP,
        author_uid INT,
        rating INT,
        PRIMARY KEY(oid),
        FOREIGN KEY(author_uid) REFERENCES User(uid)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Photo (
        pid INT NOT NULL,
        observation_oid INT,
        PRIMARY KEY(pid),
        FOREIGN KEY(observation_oid) REFERENCES Observation(oid)
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

for query in create_tables:
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Error :\n{query}\nErreur: {e}")
        exit(1)


print("All BD created")

cursor.close()
connection.close()
