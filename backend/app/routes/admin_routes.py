from flask import Blueprint, jsonify

# Create a blueprint for admin routes
bp = Blueprint("admin", __name__, url_prefix="/admin")

'''
Example
@bp.route("/dashboard", methods=["GET"])
def get_dashboard():
    """Get admin dashboard."""
    return jsonify({"message": "Admin dashboard endpoint"})

@bp.route("/stats", methods=["GET"])
def get_stats():
    """Get admin statistics."""
    return jsonify({"message": "Admin statistics endpoint"})
'''