import os

from flask import Flask, render_template, send_from_directory, session

from routes.observation import observation_bp
from routes.user import user_bp
from routes.species import species_bp
from routes.place import place_bp
from routes.photo import photo_bp
from routes.follower import follower_bp
from routes.note import note_bp

app = Flask(__name__)
app.secret_key = "5Ax83rqBr9"
app.register_blueprint(observation_bp)
app.register_blueprint(user_bp)
app.register_blueprint(species_bp)
app.register_blueprint(place_bp)
app.register_blueprint(photo_bp)
app.register_blueprint(note_bp)
app.register_blueprint(follower_bp)

@app.route("/")
def home():
    authenticated = "uid" in session
    return render_template(
        "index.html",
        authenticated=authenticated,
        user_id=session.get("uid")
    )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    os.system("python code\\database\\init_database.py")
    app.run(debug=True)
