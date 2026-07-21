import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time
from google.genai import errors
import json

# loading .env file, so that we can read the API key
load_dotenv()

# creating the client using the key from environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# updated system instruction: now asks for JSON instead of plain text
system_instruction = """You must respond with ONLY valid JSON, in exactly this format, with no extra text before or after:

{
"explanation": "a simple 2-3 sentence explanation",
"analogy": "a short, relatable analogy"
}

Example:
User: What is gravity?
{
"explanation": "Gravity is a force that pulls objects toward each other. On Earth, it pulls everything toward the ground.",
"analogy": "It's like an invisible magnet between Earth and everything on it."
}"""

prompt = input("Enter your prompt for Gemini: ")
print("Sending the prompt to Gemini...\n")

max_retries = 3  # maximum number of retries for rate limit errors

def call_gemini_with_retry(prompt):
    for attempt in range(1, max_retries + 1):
        try:
            stream = client.models.generate_content_stream(
                model="gemini-flash-latest",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    http_options=types.HttpOptions(timeout=10000)  # 10 second timeout in milliseconds
                )
            )
            full_response = ""  # collects all chunks into one string
            print("GEMINI:")
            for chunk in stream:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_response += chunk.text
                    time.sleep(0.05)
            print()
            return full_response  # now actually returns the collected text

        except errors.ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                wait_time = 5 * attempt  # waiting longer each retry
                print(f"\n[Rate limit hit. Retrying in {wait_time}s ({attempt} out of {max_retries} retries)]")
                time.sleep(wait_time)
            else:
                print(f"\n[API error: {e}]")
                return None

        except TimeoutError:
            print(f"\n[Request timed out. Retrying... ({attempt} out of {max_retries} retries)]")
            time.sleep(3)

        except Exception as e:
            print(f"\n[Unexpected error: {e}]")
            return None

    print("\n[Failed after max retries. Please try again later.]")
    return None

def validate_json_output(raw_text):
    if raw_text is None:
        return None

    # clean the output to make sure it's valid JSON
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        data = json.loads(cleaned)  # convert the cleaned string to JSON
    except json.JSONDecodeError as e:
        print(f"[Output validation failed: response was not valid JSON - {e}]")
        return None

    if "explanation" not in data or "analogy" not in data:  # check if the output contains the required fields
        print("[Output validation failed: missing required fields ('explanation', 'analogy')]")
        return None
    return data

raw_output = call_gemini_with_retry(prompt)
final_output = validate_json_output(raw_output)

if final_output:
    print("Explanation:", final_output["explanation"])
    print("Analogy:", final_output["analogy"])
else:
    print("Response is not in valid form.")