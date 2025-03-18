from flask import Blueprint, request, jsonify, render_template
from models.user_model import insert_user

signup_bp = Blueprint("signup", __name__)

@signup_bp.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@signup_bp.route("/signup", methods=["POST"])
def register_user():
    data = request.json

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    age = data.get("age")
    user_type = data.get("user_type")

    if not first_name or not last_name or not age or not user_type:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        insert_user(first_name, last_name, age, user_type)
        return jsonify({"message": "User successfully registered"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500