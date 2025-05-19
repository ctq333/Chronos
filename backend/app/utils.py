import json

def extract_json_from_string(input_text):
    """
    Extract and parse valid JSON from a given string while ignoring non-JSON content.

    Parameters:
        input_text (str): The input string containing JSON or mixed content.

    Returns:
        dict or list: The parsed JSON object (dictionary or list) if valid JSON is found.
        None: If no valid JSON is found in the input string.
    """
    try:
        # Attempt to parse the entire string as JSON
        return json.loads(input_text)
    except json.JSONDecodeError:
        # If parsing fails, try to extract valid JSON blocks
        print(input_text)
        json_start = input_text.find("[")  # Find the first JSON object start
        json_end = input_text.rfind("]")  # Find the last JSON object end

        if json_start != -1 and json_end != -1:
            # Extract the potential JSON substring
            potential_json = input_text[json_start:json_end + 1]
            try:
                return json.loads(potential_json)  # Attempt to parse the substring
            except json.JSONDecodeError:
                return None  # Return None if the substring isn't valid JSON
        return None  # Return None if no JSON-like content is found