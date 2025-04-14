from flask import Blueprint, render_template, jsonify, request, session
from datetime import datetime
import base64

from models.observation_model import (
    insert_observation,
    fetch_observations_by_user,
    fetch_observations_by_user,
    fetch_observation_by_id,
    fetch_filtered_observations,
    fetch_comments_by_observation_id,
    insert_comment,
    fetch_latest_observations
)

observation_bp = Blueprint("observation", __name__)


@observation_bp.route("/observation")
def observation():
    return render_template("observation.html")


@observation_bp.route("/user/<int:user_id>/observation", methods=["GET"])
def get_user_observation_page(user_id):
    observations = fetch_observations_by_user(user_id)

    return render_template("user_observation.html", user_id=user_id, observations=observations)


@observation_bp.route("/user/<int:user_id>/observation", methods=["POST"])
def add_user_observation(user_id):
    species = request.form.get("species")
    behavior = request.form.get("behavior")
    description = request.form.get("description")
    timestamp_raw = request.form.get("timestamp")
    pid = request.form.get("pid")
    photo_id = request.form.get("photo_id")

    if not all([species, behavior, description, timestamp_raw, pid, photo_id]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        timestamp = datetime.fromisoformat(timestamp_raw)
        pid = int(pid)
        photo_id = int(photo_id)
    except Exception as e:
        print("Conversion error:", e)
        return jsonify({"error": "Invalid data types"}), 400

    success = insert_observation(user_id, species, timestamp, behavior, description, pid, photo_id)

    if success:
        return jsonify({"message": "Observation added successfully"}), 201
    else:
        return jsonify({"error": "Failed to add observation"}), 500

@observation_bp.route("/api/user/<int:uid>/observations", methods=["GET"])
def get_user_observations(uid):
    observations = fetch_observations_by_user(uid)
    return jsonify(observations)


@observation_bp.route("/observation/<int:oid>", methods=["GET", "POST"])
def observation_page(oid):
    observation = fetch_observation_by_id(oid)
    comments = fetch_comments_by_observation_id(oid)
    userId = session.get("uid")
    observation_image = observation['image_data']
    image_data = base64.b64encode(observation_image).decode('utf-8')

    if not observation:
        return "Observation not found", 404


    return render_template("observation_page.html", observation=observation, comments=comments, userId=userId, image_data=image_data)





@observation_bp.route("/api/observations/filter", methods=["GET"])
def filter_observations():
    author = request.args.get("author")
    species = request.args.get("species")
    behavior = request.args.get("behavior")
    timestamp = request.args.get("timestamp")
    place_name = request.args.get("place_name")


    observations = fetch_filtered_observations(
        author=author,
        species=species,
        timestamp=timestamp,
        behavior=behavior,
        place_name=place_name,
    )

    print("Observations from Database:", observations)

    return jsonify(observations)

@observation_bp.route("/api/observation/<int:oid>/comments", methods=["GET"])
def get_comments_api(oid):
    comments = fetch_comments_by_observation_id(oid)
    return jsonify(comments)


@observation_bp.route("/api/observation/<int:oid>/comment", methods=["POST"])
def post_comment_api(oid):
    user_id = session.get("uid")
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    comment_text = request.form.get("comment_text")

    if not comment_text:
        return jsonify({"error": "Empty comment"}), 400

    success = insert_comment(user_id, oid, comment_text)
    if success:
        return jsonify({"message": "Comment posted successfully"}), 201
    else:
        return jsonify({"error": "Failed to post comment"}), 500


@observation_bp.route("/api/observations/latest", methods=["GET"])
def get_latest_observations():
    from models.observation_model import fetch_latest_observations
    latest = fetch_latest_observations(limit=5)

    # Encode image_data for JSON serialization
    for obs in latest:
        if obs["image_data"]:
            obs["image_data"] = base64.b64encode(obs["image_data"]).decode("utf-8")

    return jsonify(latest)
