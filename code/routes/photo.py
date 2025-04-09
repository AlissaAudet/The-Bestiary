from flask import Blueprint, jsonify, request
from models.photo_model import insert_photo

photo_bp = Blueprint('photo', __name__)


@photo_bp.route("/api/photo", methods=["POST"])
def create_photo():
    image_file = request.files.get("image")
    if not image_file:
        return jsonify({"error": "No image provided"}), 400

    photo_id = insert_photo(image_file.read())

    if photo_id:
        return jsonify({"exists": True, "photo_id": photo_id}), 201
    else:
        return jsonify({"error": "Insert failed"}), 500
