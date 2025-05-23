import os

from data import load_user_data, load_place_data, load_quebec_species, load_photo_data, load_observation_data, load_climate_data, load_ForbiddenWords_data, load_follower_data

def main():
    print("Loading user data...")
    load_user_data.load_users()

    print("Loading species data...")
    load_quebec_species.load_quebec_species()

    print("Loading climate data...")
    load_climate_data.load_climate_region()

    print("Loading place data...")
    load_place_data.load_places()

    print("Loading photo data...")
    image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/image"))
    load_photo_data.load_photos_from_directory(image_dir)

    print("Load forbidden words data...")
    words_path = os.path.join(os.path.dirname(__file__), "data/txt", "english_bad_words.txt")
    load_ForbiddenWords_data.load_forbidden_words(words_path)

    print("Loading Observation data...")
    load_observation_data.load_observations()
    print("Finished loading base observations.")
    load_observation_data.load_random_observations(100)

    print("Loading Follower data...")
    load_follower_data.load_followers()

    print("All data inserted successfully!")

if __name__ == "__main__":
    main()