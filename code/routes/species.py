from flask import Blueprint, jsonify, request
from models.species_model import get_species, search_species, get_species_info

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

@observation_bp.route("/species/<latin_name>")
def species_page(latin_name):
    latin_name = latin_name.replace('_', ' ')
    species = get_species_info(latin_name)
    return render_template("species.html", latin_name=latin_name, species=species)
