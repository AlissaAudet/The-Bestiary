import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 📂 Dossier `code/`
DATABASE_DIR = os.path.join(BASE_DIR, "Database")  # 📂 Ajoute le dossier `Database`

from flask import Flask, render_template

from routes.signup import signup_bp
from routes.login import login_bp
from routes.observation import observation_bp
from routes.user import user_bp
from routes.species import species_bp
from routes.place import place_bp

app = Flask(__name__)

app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(observation_bp)
app.register_blueprint(user_bp)
app.register_blueprint(species_bp)
app.register_blueprint(place_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    os.system("python init_database.py")
    os.system("python load_all_data.py")
    app.run(debug=True)
