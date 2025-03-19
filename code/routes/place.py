from flask import Blueprint, jsonify, request
from models.place_model import get_place_by_coordinates, insert_place, get_places
from models.database import get_db_connection

place_bp = Blueprint("place", __name__)

@place_bp.route("/api/places", methods=["GET"])
def fetch_places():
    return jsonify(get_places())

@place_bp.route("/api/places/search", methods=["GET"])
def fetch_place():
    """Check if a place exists based on name, latitude, and longitude."""
    place_name = request.args.get("place_name", "").strip()
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    if not latitude or not longitude:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT pid FROM Place 
                WHERE name = %s AND latitude = %s AND longitude = %s
            """, (place_name, latitude, longitude))
            exists = cursor.fetchone() is not None
    finally:
        connection.close()

    return jsonify({"exists": exists})

@place_bp.route("/api/places", methods=["POST"])
def create_place():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    place_name = data.get("place_name", "").strip()
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not latitude or not longitude:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    existing_place = get_place_by_coordinates(latitude, longitude, place_name)
    if existing_place:
        return jsonify({"message": "Place already exists"}), 409

    insert_place(place_name, latitude, longitude)

    return jsonify({"message": "Place added successfully"}), 201


