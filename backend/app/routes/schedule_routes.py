from flask import Blueprint, jsonify

# Create a blueprint for schedule routes
bp = Blueprint("schedule", __name__, url_prefix="/schedule")