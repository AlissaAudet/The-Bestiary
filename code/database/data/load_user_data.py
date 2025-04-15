import sys
import os
#
#doit etre modif pour avoir les clé comme attibut

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from models.database import get_db_connection


def load_users():
    connection = get_db_connection()
    cursor = connection.cursor()

    users = [
        ("Stephanie",	"Tremblay",	"stephanie@gmail.com",	20,	"$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Scientist"),
        ("Martine", "Leclerc", "martine@gmail.com", 40, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Scientist"),
        ("Julien", "Moreau", "julien.moreau@gmail.com", 35, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Passionate"),
        ("Sophie", "Dubois", "sophie.dubois@gmail.com", 29, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Scientist"),
        ("Lucas", "Lemoine", "lucas.lemoine@gmail.com", 42, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Passionate"),
        ("Claire", "Gagnon", "claire.gagnon@gmail.com", 33, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Scientist"),
        ("Antoine", "Roy", "antoine.roy@gmail.com", 37, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Passionate"),
        ("Isabelle", "Richard", "isabelle.richard@gmail.com", 31, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Scientist"),
        ("Maxime", "Poirier", "maxime.poirier@gmail.com", 45, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Passionate"),
        ("Camille", "Fortin", "camille.fortin@gmail.com", 28, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Scientist"),
        ("Hugo", "Girard", "hugo.girard@gmail.com", 39, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Passionate"),
        ("Elodie", "Pelletier", "elodie.pelletier@gmail.com", 26, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Scientist"),
        ("Thomas", "Bergeron", "thomas.bergeron@gmail.com", 34, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Passionate"),
        ("Geneviève", "Lévesque", "genevieve.levesque@gmail.com", 41, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Scientist"),
        ("Alexandre", "Côté", "alex.cote@gmail.com", 30, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Passionate"),
        ("Julie", "Boucher", "julie.boucher@gmail.com", 38, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Scientist"),
        ("Marc", "Tremblay", "marc.tremblay@gmail.com", 32, "$2b$12$W9gyS2gIGTkeYo1v0BXid.G5U9AZKk4K7jwzOB17JdyzwfyixKqYe", "Passionate")
    ]

    query = """
        INSERT INTO User (first_name, last_name, email, age, password_hash, user_type) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(query, users)
        connection.commit()
        print("users added successfully!")
    except Exception as e:
        print(f"Error inserting users: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    load_users()
