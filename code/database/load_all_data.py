from data import load_user_data, load_species_data, load_place_data, load_quebec_species

def main():
    print("Loading user data...")
    load_user_data.load_users()

    print("Loading species data...")
    # load_species_data.load_species()
    load_quebec_species.load_quebec_species()

    print("Loading place data...")
    load_place_data.load_places()

    print("All data inserted successfully!")

if __name__ == "__main__":
    main()