from flask import Blueprint, jsonify, render_template, request, make_response, redirect, url_for, session
import bcrypt
import jwt
import datetime
from models.user_model import get_users, insert_user, get_user_by_id, search_users, get_user_by_email

user_bp = Blueprint("user", __name__)


SECRET_KEY = "SHAI-HULUD"

@user_bp.route("/api/users", methods=["GET"])
def fetch_users():
    users = get_users()
    return jsonify([
        {"uid": user["uid"], "first_name": user["first_name"], "last_name": user["last_name"]}
        for user in users
    ])


@user_bp.route("/api/users/search", methods=["GET"])
def search_users_api():
    query = request.args.get("q", "").strip()

    if not query:
        print("No query received in /api/users/search")
        return jsonify([])

    users = search_users(query)
    print(f"API returning users: {users}")

    return jsonify(users)


@user_bp.route("/user/<int:uid>", methods=["GET"])
def user_page(uid):
    token = request.cookies.get("auth_token")
    authenticated = False
    authorized = False
    user_id = None

    if token:
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded["user_id"]
            authenticated = True
            authorized = (user_id == uid)
        except jwt.ExpiredSignatureError:
            print("Token expired!")
        except jwt.InvalidTokenError:
            print("Invalid token!")

    user = get_user_by_id(uid)
    if user:
        return render_template("user.html", user=user, authenticated=authenticated, authorized=authorized,
                               user_id=user_id,
                               profile_uid=uid
                               )

    return "User not found", 404

@user_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@user_bp.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")


@user_bp.route("/signup", methods=["POST"])
def register_user():
    data = request.json
    print("Received signup request:", data)

    if not data:
        return jsonify({"error": "No data received"}), 400

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    age = data.get("age")
    password = data.get("password")
    user_type = data.get("user_type")

    if not first_name or not last_name or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        insert_user(first_name, last_name, email, age, password, user_type)
        return jsonify({"message": "User successfully registered"}), 201
    except Exception as e:
        print(f"Error inserting user: {e}")
        return jsonify({"error": str(e)}), 500


@user_bp.route("/login", methods=["POST"])
def login_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = get_user_by_email(email)
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return jsonify({"error": "Invalid email or password"}), 401

    token = jwt.encode({
        "user_id": user["uid"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    response = make_response(jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user["uid"]
    }))
    session["uid"] = user["uid"]
    response.set_cookie("auth_token", token, httponly=True, secure=True, samesite="None")
    return response

@user_bp.route("/logout", methods=["POST"])
def logout_user():
    session.pop("uid", None)
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.set_cookie("auth_token", "", expires=0, httponly=True, secure=True, samesite="Lax")
    return response


@user_bp.route("/check_auth", methods=["GET"])
def check_auth():
    token = request.cookies.get("auth_token")

    if not token:
        return jsonify({"authenticated": False}), 401

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"authenticated": True, "user_id": decoded["user_id"]})
    except jwt.ExpiredSignatureError:
        return jsonify({"authenticated": False, "error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"authenticated": False, "error": "Invalid token"}), 40