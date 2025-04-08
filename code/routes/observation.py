from flask import Blueprint, render_template, jsonify, request

from models.observation_model import (
    insert_observation,
    insert_photo,
    fetch_observations_by_user,
    fetch_observations_by_user,
    fetch_observation_by_id)
observation_bp = Blueprint("observation", __name__)

@observation_bp.route("/user/<int:user_id>/observation", methods=["GET"])
def get_user_observation_page(user_id):
    observations = fetch_observations_by_user(user_id)

    return render_template("user_observation.html", user_id=user_id, observations=observations)

# @observation_bp.route("/user/<int:user_id>/observation", methods=["POST"])
# def add_user_observation(user_id):
#     observations = fetch_observations_by_user(user_id)
#     return render_template("user_observation.html", user_id=user_id, observations=observations)
#


@observation_bp.route("/user/<int:user_id>/observation", methods=["POST"])
def add_user_observation(user_id):
    """
    Add a new observation for a user.
    This endpoint now supports both JSON and multipart/form-data requests (allowing file uploads).
    """
    # Check if the content is multipart (for file upload) or JSON.
    if request.content_type.startswith("multipart/form-data"):
        species = request.form.get("species")
        timestamp = request.form.get("timestamp")
        behavior = request.form.get("behavior")
        description = request.form.get("description")
        pid = request.form.get("pid")
        image_file = request.files.get("image")
        image_data = image_file.read() if image_file and image_file.filename else None
    else:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400
        species = data.get("species")
        behavior = data.get("behavior")
        description = data.get("description")
        pid = data.get("pid")
        image_data = None  # No file sent in JSON requests

    # Check that all required fields are present
    if not all([species, behavior, description, pid]):
        return jsonify({"error": "Missing required fields"}), 400

    # Insert the observation in the database
    obs_id = insert_observation(user_id, species, behavior, description, pid)

    # If an image was provided and observation insertion succeeded, save the image
    if obs_id and image_data:
        photo_success = insert_photo(obs_id, image_data)
        if not photo_success:
            # Here you may decide to roll back the observation or notify the user that only the observation was saved.
            return jsonify({"error": "Observation added but failed to add photo"}), 500

    if obs_id:
        return jsonify({"message": "Observation added successfully", "id": obs_id}), 201
    else:
        return jsonify({"error": "Failed to add observation"}), 500

@observation_bp.route("/api/user/<int:uid>/observations", methods=["GET"])
def get_user_observations(uid):
    observations = fetch_observations_by_user(uid)
    return jsonify(observations)


@observation_bp.route("/observation/<int:oid>", methods=["GET"])
def observation_page(oid):
    observation = fetch_observation_by_id(oid)

    if not observation:
        return "Observation not found", 404

    return render_template("observation_page.html", observation=observation)


