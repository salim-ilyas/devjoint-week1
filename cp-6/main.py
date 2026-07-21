import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time
from google.genai import errors
import json

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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

max_retries = 3

# gemini 3.5 flash pricing
input_price_per_million = 0.75
output_price_per_million = 4.5

def call_gemini_with_retry(prompt):
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    http_options=types.HttpOptions(timeout=10000)
                )
            )
            return response

        except errors.ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                wait_time = 5 * attempt
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
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"[Output validation failed: response was not valid JSON - {e}]")
        return None
    if "explanation" not in data or "analogy" not in data:
        print("[Output validation failed: missing required fields ('explanation', 'analogy')]")
        return None
    return data


def log_token_usage(response):
    # logging token usage and estimated cost
    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count
    output_tokens = usage.candidates_token_count
    thinking_tokens = usage.thoughts_token_count or 0
    total_tokens = usage.total_token_count

    input_cost = (input_tokens / 1_000_000) * input_price_per_million
    output_cost = ((output_tokens + thinking_tokens) / 1_000_000) * output_price_per_million
    total_cost = input_cost + output_cost

    print("\nToken Usage:")
    print(f"Input tokens:    {input_tokens}")
    print(f"Output tokens:   {output_tokens}")
    print(f"Thinking tokens: {thinking_tokens}")
    print(f"Total tokens:    {total_tokens}")
    print(f"Estimated cost:  ${total_cost:.6f}")

response = call_gemini_with_retry(prompt)

if response:
    final_output = validate_json_output(response.text)
    if final_output:
        print("Explanation:", final_output["explanation"])
        print("Analogy:", final_output["analogy"])
    else:
        print("Response is not in valid form.")

    log_token_usage(response)
else:
    print("No response received.")