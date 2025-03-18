from flask import Blueprint, jsonify, render_template, request
from models.user_model import get_users, insert_user

user_bp = Blueprint("user", __name__)

@user_bp.route("/api/users", methods=["GET"])
def fetch_users():

    return jsonify(get_users())
@user_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@user_bp.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@user_bp.route("/signup", methods=["POST"])
def register_user():
    data = request.json

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    age = data.get("age")
    user_type = data.get("user_type")

    if not first_name or not last_name or not age or not user_type or not email:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        insert_user(first_name, last_name, age, user_type)
        return jsonify({"message": "User successfully registered"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500