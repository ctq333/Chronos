from google import genai
import os
from datetime import datetime

# Load the API key from the environment or fallback to a default key
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "your_default_key_here")

# Initialize the GenAI client
client = genai.Client(api_key=GENAI_API_KEY)

current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
TIME_PROMPT_TEMPLATE = f"""
The current time is {current_time_str}. If the date is not provided, please use that time as a reference to determine the date, month, year, and time.
"""
# Prompt template for GenAI


def generate_content(prompt, content):
    """Generate content using GenAI."""
    try:
        # Create the prompt
        combined_prompt = TIME_PROMPT_TEMPLATE + prompt + content

        # Call the GenAI API
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=combined_prompt
        )

        # Return the raw response text
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error generating content: {str(e)}")