import data.load_user_data
import data.load_species_data
import data.load_place_data

print("Loading user data...")
data.load_user_data.load_users()

print("Loading species data...")
data.load_species_data.load_species()

print("Loading place data...")
data.load_place_data.load_places()

print("All data inserted successfully!")
