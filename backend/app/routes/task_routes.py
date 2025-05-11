from flask import Blueprint, jsonify

# Create a blueprint for task routes
bp = Blueprint("task", __name__, url_prefix="/task")
'''
Example
@bp.route("/list", methods=["GET"])
def list_tasks():
    """List all tasks."""
    return jsonify({"message": "List of tasks endpoint"})
'''