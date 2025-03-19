from flask import Blueprint, jsonify, request
from models.species_model import get_species, search_species

species_bp = Blueprint("species", __name__)

@species_bp.route("/api/species", methods=["GET"])
def fetch_species():
    return jsonify(get_species())

@species_bp.route("/api/species/search", methods=["GET"])
def search_species_api():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify([])

    species = search_species(query)
    return jsonify(species)
