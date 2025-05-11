from flask import Blueprint, jsonify

# Create a blueprint for auth routes
bp = Blueprint("auth", __name__, url_prefix="/auth")