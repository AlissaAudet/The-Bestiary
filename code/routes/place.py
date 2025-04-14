from flask import Blueprint, jsonify, request
from models.place_model import get_place_by_coordinates, insert_place, get_places

place_bp = Blueprint("place", __name__)

@place_bp.route("/api/places/search", methods=["GET"])
def search_place():
    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)
    name = request.args.get("place_name", type=str)

    if latitude is None or longitude is None or name is None:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        pid = get_place_by_coordinates(latitude, longitude, name)
        if pid:
            return jsonify({"exists": True, "pid": pid})
        else:
            return jsonify({"exists": False})
    except Exception as e:
        print("Error in /api/places/search:", e)
        return jsonify({"exists": False, "error": str(e)}), 500




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