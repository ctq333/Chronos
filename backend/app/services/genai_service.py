from google import genai
import os

# Load the API key from the environment or fallback to a default key
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "your_default_key_here")

# Initialize the GenAI client
client = genai.Client(api_key=GENAI_API_KEY)

# Prompt template for GenAI
EVENT_PROMPT_TEMPLATE = """
Now you will serve as a backend. You should reply to me only in JSON format, no extra sentences. I will send you a JSON template to fill in, along with a paragraph, which can contain topic, data and time range, location, links. You need to recognize those things in the text, and return them in JSON. JSON fields can be left empty if not recognized, except for startTime and endTime, which should be filled with the date recognized, and time should be 00:00 if not recognized. If the event mentioned in text is not a one or multi-day event and also a start time is recognized but no end time is recognized, set end time at one hour later. The language you fill into JSON should be the language you recognized in the text. 

JSON Schema:
{
  "topic": str,
  "startTime": str,    # Use "yyyy-mm-dd hh:mm" format; if no time is recognized, use "00:00". If no date is recognized, use today's date.
  "endTime": str,      # Use "yyyy-mm-dd hh:mm" format; if no end time is found, set it to "23:59".
  "location": str,     # Recognized location in the text.
  "links": list[str],  # List of recognized links in the text.
  "notes": str         # Key points summarized as a string.
}

also no ```json``` or ```text``` or ```python``` in the response, just pure json
"""

def generate_content(paragraph):
    """Generate content using GenAI."""
    try:
        # Create the prompt
        prompt = EVENT_PROMPT_TEMPLATE + paragraph

        # Call the GenAI API
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )

        # Return the raw response text
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error generating content: {str(e)}")