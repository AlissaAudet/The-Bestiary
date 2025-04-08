import os

from flask import Flask, render_template, send_from_directory

from routes.observation import observation_bp
from routes.user import user_bp
from routes.species import species_bp
from routes.place import place_bp
from routes.photo import photo_bp

app = Flask(__name__)
app.register_blueprint(observation_bp)
app.register_blueprint(user_bp)
app.register_blueprint(species_bp)
app.register_blueprint(place_bp)
app.register_blueprint(photo_bp)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    os.system("python code\\database\\init_database.py")
    app.run(debug=True)
