import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from models.database import get_db_connection

def load_species():
    connection = get_db_connection()
    cursor = connection.cursor()

    species = [
        ("Panthera leo", "Lion", "Panthera", "Felidae", "Carnivora", "Mammalia", "Chordata", "Animal", "King of the jungle."),
        ("Canis lupus", "Wolf", "Canis", "Canidae", "Carnivora", "Mammalia", "Chordata", "Animal", "Pack animal and apex predator."),
        ("Ursus arctos", "Brown Bear", "Ursus", "Ursidae", "Carnivora", "Mammalia", "Chordata", "Animal", "Large bear species."),
        ("Giraffa camelopardalis", "Giraffe", "Giraffa", "Giraffidae", "Artiodactyla", "Mammalia", "Chordata", "Animal", "Tallest land animal."),
        ("Equus ferus caballus", "Horse", "Equus", "Equidae", "Perissodactyla", "Mammalia", "Chordata", "Animal", "Domesticated for riding."),
        ("Balaenoptera musculus", "Blue Whale", "Balaenoptera", "Balaenopteridae", "Cetacea", "Mammalia", "Chordata", "Animal", "Largest animal on Earth."),
        ("Falco peregrinus", "Peregrine Falcon", "Falco", "Falconidae", "Falconiformes", "Aves", "Chordata", "Animal", "Fastest bird."),
        ("Haliaeetus leucocephalus", "Bald Eagle", "Haliaeetus", "Accipitridae", "Accipitriformes", "Aves", "Chordata", "Animal", "National bird of the USA."),
        ("Loxodonta africana", "African Elephant", "Loxodonta", "Elephantidae", "Proboscidea", "Mammalia", "Chordata", "Animal", "Largest land mammal."),
        ("Ailuropoda melanoleuca", "Giant Panda", "Ailuropoda", "Ursidae", "Carnivora", "Mammalia", "Chordata", "Animal", "Loves eating bamboo.")
    ]

    query = """
        INSERT INTO Species (latin_name, name, genus, family, order_name, class_name, phylum, kingdom, description) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(query, species)
        connection.commit()
        print("10 species added successfully!")
    except Exception as e:
        print(f"Error inserting species: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    load_species()
