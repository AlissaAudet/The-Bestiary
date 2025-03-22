from flask import Blueprint, jsonify, request
from models.place_model import get_place_by_coordinates, insert_place, get_places

place_bp = Blueprint("place", __name__)


@place_bp.route("/api/places/search", methods=["GET"])
def fetch_place():
    place_name = request.args.get("place_name", "").strip()
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    if not latitude or not longitude:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    pid = get_place_by_coordinates(latitude, longitude, place_name)

    if pid is not None:
        return jsonify({"exists": True, "pid": pid})
    else:
        return jsonify({"exists": False})



@place_bp.route("/api/places", methods=["POST"])
def create_place():
    data = request.json
    place_name = data.get("place_name")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not place_name or not latitude or not longitude:
        return jsonify({"error": "Missing required fields"}), 400

    pid = insert_place(place_name, latitude, longitude)

    if pid:
        return jsonify({"message": "Place added successfully", "pid": pid}), 201
    else:
        return jsonify({"error": "Failed to add place"}), 500

