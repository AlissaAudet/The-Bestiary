from flask import Flask, render_template

from routes.signup import signup_bp
from routes.login import login_bp

app = Flask(__name__)

app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
