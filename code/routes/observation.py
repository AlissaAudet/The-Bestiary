from flask import Blueprint, render_template, jsonify, request

from models.observation_model import insert_observation, fetch_observations_by_user
observation_bp = Blueprint("observation", __name__)

@observation_bp.route("/observation", methods=["GET"])
def observation_page():
    return render_template("observation.html")

@observation_bp.route("/user/<int:user_id>/observation", methods=["GET"])
def get_user_observation_page(user_id):
    observations = fetch_observations_by_user(user_id)

    return render_template("user_observation.html", user_id=user_id, observations=observations)


@observation_bp.route("/api/observations", methods=["POST"])
def add_observation():
    data = request.json

    if not all(key in data for key in ["user_id", "species", "timestamp", "behavior", "description", "pid"]):
        return jsonify({"error": "Missing required fields"}), 400

    success = insert_observation(
        data["user_id"],
        data["species"],
        data["timestamp"],
        data["behavior"],
        data["description"],
        data["pid"]
    )

    if success:
        return jsonify({"message": "Observation recorded successfully"}), 201
    else:
        return jsonify({"error": "database error"}), 500
