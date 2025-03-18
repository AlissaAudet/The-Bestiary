import os

from flask import Flask, render_template

from routes.observation import observation_bp
from routes.user import user_bp
from routes.species import species_bp
from routes.place import place_bp

app = Flask(__name__)
app.register_blueprint(observation_bp)
app.register_blueprint(user_bp)
app.register_blueprint(species_bp)
app.register_blueprint(place_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    os.system("python init_database.py")
    app.run(debug=True)
