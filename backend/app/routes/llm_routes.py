from flask import Blueprint, jsonify, request
from app.services.genai_service import generate_content
from app.utils import extract_json_from_string

EVENT_PROMPT_TEMPLATE = """
Now you will serve as a backend. You should reply to me only in JSON format, no extra sentences. I will send you a JSON template to fill in, along with a paragraph, which can contain multiple events, each event can include a topic, date and time range, location, website links. You need to recognize those things in the paraghaph accurately, without any mistake and return them in JSON. JSON fields can be left empty if not recognized, except for startTime and endTime, which should be filled with the recognized date, and you can choose an proper start time. If the event mentioned in text is not a one or multi-day event and also a start time is recognized but no end time is recognized, set end time at one hour later. The language you fill into JSON should be the language you recognized in the text. 

JSON Schema:
[
    {
        "topic": str,
        "startTime": str,    # Use "yyyy-mm-dd hh:mm" format; if no time is recognized, choose a proper start time. If no date is recognized, use today's date.
        "endTime": str,      # Use "yyyy-mm-dd hh:mm" format; if no end time is found, set it to "23:59" or a more proper one.
        "location": str,     # Recognized location in the text.
        "links": list[str],  # List of recognized links in the text.
        "notes": str         # Key points for one single event summarized as a string.
    },
    {
        "topic": str,
        "startTime": str,    # Use "yyyy-mm-dd hh:mm" format; if no time is recognized, choose a proper start time. If no date is recognized, use today's date.
        "endTime": str,      # Use "yyyy-mm-dd hh:mm" format; if no end time is found, set it to "23:59" or a more proper one.
        "location": str,     # Recognized location in the text.
        "links": list[str],  # List of recognized links in the text.
        "notes": str         # Key points one single event summarized as a string,.
    },
    ...
]

also no ```json``` or ```text``` or ```python``` in the response, just pure json, the following is the paragraph:
"""

TASK_PROMPT_TEMPLATE = """
Now you will serve as a backend. You should reply to me only in JSON format, no extra sentences. I will send you a JSON template to fill in, along with a paragraph, which can contain multiple tasks, each task can include a task heading, plan date, due date, priority, tags, notes. You need to recognize those things in the paraghaph accurately, without any mistake and return them in JSON. JSON fields can be left empty if not recognized, except for planDate and dueTime, which should be filled with the recognized date. You can choose an proper plan date if no plan date is provided, and set due date to one day later if no due date is provided. The language you used to fill into JSON should be the language you recognized in the text. 

JSON Schema:
[
    {
        "heading": str,
        "planDate": str,    # Use "yyyy-mm-dd" format; if no plan date is recognized, choose a proper plan date. If no date is recognized, use today's date.
        "dueDate": str,      # Use "yyyy-mm-dd" format; if no due date is found, set it to one day later.
        "priority": int,     # 0=low, 1=medium, 2=high, 3=urgent
        "tags": str,   # List of recognized tags in the text, use "," to split them.
        "notes": str         # Key points for one single task summarized as a string.
    },
    {
        "heading": str,
        "planDate": str,    # Use "yyyy-mm-dd" format; if no plan date is recognized, choose a proper plan date. If no date is recognized, use today's date.
        "dueDate": str,      # Use "yyyy-mm-dd" format; if no due date is found, set it to one day later.
        "priority": int,     # 0=low, 1=medium, 2=high, 3=urgent
        "tags": str,   # List of recognized tags in the text, use "," to split them.
        "notes": str         # Key points for one single task summarized as a string.
    },
    ...
]

also no ```json``` or ```text``` or ```python``` in the response, just pure json, the following is the paragraph:
"""
# Create a blueprint for the main routes
bp = Blueprint("llm", __name__, url_prefix="/llm")

@bp.route("/createSchedule", methods=["POST"])
def create_schedule():
    try:
        # Get input paragraph
        input_data = request.json
        paragraph = input_data.get("paragraph", "")

        if not paragraph:
            return jsonify({"error": "No paragraph provided"}), 400

        # Call the GenAI service
        response_text = generate_content(EVENT_PROMPT_TEMPLATE, paragraph)

        # Parse and return the JSON response
        parsed_response = extract_json_from_string(response_text)
        if parsed_response:
            return jsonify(parsed_response)
        else:
            return jsonify({"error": "Invalid JSON format in AI response", "details": response_text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bp.route("/createTask", methods=["POST"])
def create_task():
    try:
        # Get input paragraph
        input_data = request.json
        paragraph = input_data.get("paragraph", "")

        if not paragraph:
            return jsonify({"error": "No paragraph provided"}), 400

        # Call the GenAI service
        response_text = generate_content(TASK_PROMPT_TEMPLATE, paragraph)

        # Parse and return the JSON response
        parsed_response = extract_json_from_string(response_text)
        if parsed_response:
            return jsonify(parsed_response)
        else:
            return jsonify({"error": "Invalid JSON format in AI response", "details": response_text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500