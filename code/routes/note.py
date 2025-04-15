from flask import Blueprint, render_template, jsonify, request
from models.note_model import (insert_or_update_note)

note_bp = Blueprint("note", __name__)

@note_bp.route("/observation/<int:oid>/", methods=["POST"])
def add_observation_rating(oid):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Must submit a valid rating."}), 400
    
    nid = data.get("nid")
    observation_oid = oid
    user_uid = data.get("user.uid")
    rating = data.get("note")

    if not all([nid, observation_oid, user_uid, rating]):
        return jsonify({"error": "Note need to be between 1 and 5"}), 400

    noteInsert = insert_or_update_note(nid, observation_oid, user_uid, rating)

    if noteInsert:
        return jsonify({"message": "Rating submitted successfully", "id": noteInsert}), 201
    else:
        return jsonify({"error": "Failed to submit rating"}), 500
    

