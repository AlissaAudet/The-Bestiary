from flask import Blueprint, jsonify, request
from models.place_model import get_place_by_coordinates, insert_place, get_places

place_bp = Blueprint("place", __name__)

@place_bp.route("/api/places", methods=["GET"])
def fetch_places():
    return jsonify(get_places())

@place_bp.route("/api/places/search", methods=["GET"])
def fetch_place():
    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)
    name = request.args.get("name", type=str)

    if latitude is None or longitude is None or name is None:
        return jsonify({"error": "Missing latitude, longitude, or name"}), 400

    place = get_place_by_coordinates(latitude, longitude, name)
    if place:
        return jsonify({"pid": place["pid"]})
    else:
        return jsonify({"error": "Place not found"}), 404


@place_bp.route("/api/places", methods=["POST"])
def create_place():
    data = request.json

    if not all(k in data for k in ["latitude", "longitude", "name"]):
        print("Missing fields in /api/places request:", data)
        return jsonify({"error": "Missing fields"}), 400

    print(f"Creating place: {data['name']} (lat: {data['latitude']}, lon: {data['longitude']})")

    pid = insert_place(data["name"], data["latitude"], data["longitude"])

    if pid:
        print(f" Place successfully created: {data['name']} (pid: {pid})")
        return jsonify({"message": "Place created successfully", "pid": pid}), 201
    else:
        print("Failed to create place")
        return jsonify({"error": "database error"}), 500
