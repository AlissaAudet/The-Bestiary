import os
import sys

import requests
import pymysql

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


def load_quebec_species():
    resource_id = "73060a93-990c-4529-b87e-9aaf6772cd06"
    base_url = "https://www.donneesquebec.ca/recherche/api/3/action/datastore_search"

    offset = 0
    limit = 100
    all_records = []

    while True:
        params = {
            "resource_id": resource_id,
            "limit": limit,
            "offset": offset
        }
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print("Error fetching data from the API")
            break
        data = response.json()
        records = data["result"]["records"]
        if not records:
            break
        all_records.extend(records)
        offset += limit

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="glo_2005_projet",
        autocommit=True
    )
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO Species (latin_name, name, genus, family, order_name, class_name, phylum, kingdom, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    inserted_latin_names = set()

    for record in all_records:
        latin_name = (record.get("Nom_scientifique") or "").strip()
        if not latin_name:
            continue  # Skip if no latin name provided

        if latin_name in inserted_latin_names:
            print(f"Skipping duplicate: {latin_name}")
            continue

        inserted_latin_names.add(latin_name)

        name = (record.get("Nom_francais") or "").strip()

        classification = record.get("Classification hiérarchique", "")
        classification_parts = [part.strip() for part in classification.split(";")] if classification else []
        class_name = classification_parts[0] if len(classification_parts) >= 1 else ""
        order_name = classification_parts[1] if len(classification_parts) >= 2 else ""
        family = classification_parts[2] if len(classification_parts) >= 3 else ""
        genus = classification_parts[3] if len(classification_parts) >= 4 else ""

        # Default values
        phylum = "Chordata"
        kingdom = "Animal"

        description = (record.get("Commentaires") or "").strip()[:500]

        try:
            cursor.execute(insert_query,
                           (latin_name, name, genus, family, order_name, class_name, phylum, kingdom, description))
        except Exception as e:
            print("Error inserting record:", record)
            print(e)
    cursor.close()
    connection.close()
    print("Species table populated successfully!")


if __name__ == "__main__":
    load_quebec_species()