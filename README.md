# 🦉 The Bestiary

The Bestiary is a collaborative web platform for recording and sharing geolocated wildlife observations across Quebec. Designed for both nature enthusiasts and amateur scientists, it allows users to publish animal sightings, rate and comment on them, follow other users, and explore biodiversity data through search and filtering tools. The goal is to bridge the gap between citizen science and social networking by creating a community-driven biodiversity catalog.

# Setup 

### MySQL Setup

To set your root password to "root", run the following command in your MySQL terminal (as root):

    ALTER USER 'root'@'localhost' IDENTIFIED BY 'root'; 
    FLUSH PRIVILEGES;

### Requirements

To generate a list of dependencies (in your own environment):

    pip freeze > requirements.txt

To install dependencies:

    pip install -r requirements.txt

## Running the Application

    python code/app.py

Once launched, the application will be available at:

http://127.0.0.1:5000

app.py runs the following steps:

    init_database.py — resets and initializes the database structure.

    load_all_data.py — loads mock/fake data for development and testing.

    Starts the Flask server.

## Project Structure
Layers

    templates/ — Contains HTML templates used to render pages.

    static/ — Contains static JavaScript files for API interactions and UI logic.

    routes/ — Defines Flask routes, organized by table (e.g., user, observation).

    models/ — Database logic (CRUD operations), also organized by table.

    database/ — Handles database initialization, triggers, functions, and data loading scripts.

# Pictures of some of the pages

### Home page

![image](https://github.com/user-attachments/assets/71b4372e-d160-48c7-9a53-1c17105f1d7a)


### Search Observation Page

![image](https://github.com/user-attachments/assets/ad8352a9-84fc-45fe-8d90-ea71b58d92f1)


### User page

![image](https://github.com/user-attachments/assets/5b73cb5e-0b6b-4631-ab18-deaffabffb99)


### Add observation page

![image](https://github.com/user-attachments/assets/f6aef131-d09d-42dd-81e5-3fa74c8b55ce)


### Observation Page

![image](https://github.com/user-attachments/assets/fbd7a427-a30f-48de-af61-284ece159c8f)

### Sign Up

![image](https://github.com/user-attachments/assets/17441901-c4bf-45eb-b619-a0a2923015c9)




