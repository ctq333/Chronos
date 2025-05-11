from flask import Blueprint, jsonify, request
from app.services.genai_service import generate_content
from app.utils import extract_json_from_string

# Create a blueprint for the main routes
bp = Blueprint("llm", __name__, url_prefix="/llm")

@bp.route("/createSchedule", methods=["POST"])
def process_input():
    try:
        # Get input paragraph
        input_data = request.json
        paragraph = input_data.get("paragraph", "")

        if not paragraph:
            return jsonify({"error": "No paragraph provided"}), 400

        # Call the GenAI service
        response_text = generate_content(paragraph)

        # Parse and return the JSON response
        parsed_response = extract_json_from_string(response_text)
        if parsed_response:
            return jsonify(parsed_response)
        else:
            return jsonify({"error": "Invalid JSON format in AI response", "details": response_text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500