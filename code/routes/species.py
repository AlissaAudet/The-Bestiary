from flask import Blueprint, jsonify
from models.species_model import get_species

species_bp = Blueprint("species", __name__)

@species_bp.route("/api/species", methods=["GET"])
def fetch_species():
    return jsonify(get_species())
