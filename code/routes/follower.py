import jwt

from flask import Blueprint, request, jsonify, session
from models.follower_model import follow_user, unfollow_user, get_followers, get_following, is_following_user

follower_bp = Blueprint("follower", __name__)

@follower_bp.route("/follow/<int:target_uid>", methods=["POST"])
def follow(target_uid):
    current_uid = session.get("uid")
    if not current_uid:
        return jsonify({"error": "Authentication required"}), 401

    if current_uid == target_uid:
        return jsonify({"error": "You cannot follow yourself."}), 400

    success = follow_user(current_uid, target_uid)
    if success:
        return jsonify({"message": f"You are now following user {target_uid}."}), 200
    else:
        return jsonify({"error": "Failed to follow user."}), 500

@follower_bp.route("/unfollow/<int:target_uid>", methods=["POST"])
def unfollow(target_uid):
    current_uid = session.get("uid")
    if not current_uid:
        return jsonify({"error": "Authentication required"}), 401

    success = unfollow_user(current_uid, target_uid)
    if success:
        return jsonify({"message": f"You unfollowed user {target_uid}."}), 200
    else:
        return jsonify({"error": "Failed to unfollow user."}), 500


@follower_bp.route("/api/followers/<int:uid>", methods=["GET"])
def get_followers_route(uid):
    if not session.get("uid"):
        return jsonify({"error": "Authentication required"}), 401

    followers = get_followers(uid)
    return jsonify(followers)


@follower_bp.route("/api/following/<int:uid>", methods=["GET"])
def get_following_route(uid):
    if not session.get("uid"):
        return jsonify({"error": "Authentication required"}), 401

    following = get_following(uid)
    return jsonify(following)


@follower_bp.route("/is_following/<int:target_uid>", methods=["GET"])
def is_following_route(target_uid):
    current_uid = session.get("uid")
    if not current_uid:
        return jsonify({"error": "Authentication required"}), 401

    is_following = is_following_user(current_uid, target_uid)
    return jsonify({"is_following": is_following})
