import os
import random
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors as genai_errors
import time
from pydantic import BaseModel, ValidationError

# loading .env file so that we can read the API key
load_dotenv()
# checking GEMINI_API_KEY exists before creating the client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("No API key found.")
# creating the client using the key from environment variable
client = genai.Client(api_key=api_key)

# pydantic model for validating the structured response from Gemini
class ExplanationResponse(BaseModel):
    explanation: str
    analogy: str

# setting the system instruction
system_instruction = ("""
Given a concept, provide a simple explanation and a short, relatable analogy.

Example 1:
User: What is gravity?
{"explanation": "Gravity is a force that pulls objects toward each other. On Earth, it pulls everything toward the ground.", "analogy": "It's like an invisible magnet between Earth and everything on it."}

Example 2:
User: What is an API?
{"explanation": "An API lets two computer programs talk to each other and exchange information.", "analogy": "It's like a waiter taking your order to the kitchen and bringing back your food."}

Example 3:
User: What is electricity?
{"explanation": "Electricity is the flow of tiny particles called electrons through a wire, which powers devices.", "analogy": "It's like water flowing through a pipe, powering anything it passes through."}""")

prompt = input("Enter your prompt for Gemini: ")
print("Sending the prompt to Gemini...")
print("\nGEMINI:")

MAX_RETRIES = 4
BASE_DELAY = 1


def get_status_code(error):
    return getattr(error, "code", None) or getattr(error, "status_code", None)

def is_retryable_api_error(error):
    status = get_status_code(error)
    if status == 429:
        return True
    if status is not None and 500 <= status < 600:
        return True
    return False


def get_retry_delay(error, attempt):
    retry_after = getattr(error, "retry_after", None)
    if retry_after:
        return float(retry_after)
    delay = BASE_DELAY * (2 ** attempt)
    jitter = random.uniform(0, delay * 0.5)
    return delay + jitter


collected_text = []
finish_reason = None
interrupted = False
attempt = 0

while True:
    collected_text = []
    finish_reason = None

    try:
        stream = client.models.generate_content_stream(
            model="gemini-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                # specifying the response format and schema for structured output
                response_mime_type="application/json",
                response_schema=ExplanationResponse,
            )
        )

        for chunk in stream:
            if not chunk.candidates:
                continue
            candidate = chunk.candidates[0]

            # printing text as it streams in, flushing so it shows up immediately
            if chunk.text:
                print(chunk.text, end="", flush=True)
                collected_text.append(chunk.text)

            if candidate.finish_reason is not None:
                finish_reason = candidate.finish_reason
        break

    except KeyboardInterrupt:
        interrupted = True
        print("\n[Streaming interrupted by user.]")
        break

    except (TimeoutError, ConnectionError) as e:
        if attempt < MAX_RETRIES:
            delay = get_retry_delay(e, attempt)
            print(f"\n[Network/timeout error. Retrying in {delay:.1f}s(attempt {attempt + 1}/{MAX_RETRIES})]")
            time.sleep(delay)
            attempt += 1
            continue
        interrupted = True
        print(f"\n[Streaming failed after {MAX_RETRIES} retries: {e}]")
        break

    except genai_errors.APIError as e:
        if is_retryable_api_error(e) and attempt < MAX_RETRIES:
            delay = get_retry_delay(e, attempt)
            print(f"\n[API error {get_status_code(e)}. Retrying in {delay:.1f}s (attempt {attempt + 1}/{MAX_RETRIES})]")
            time.sleep(delay)
            attempt += 1
            continue
        interrupted = True
        print(f"\n[Streaming interrupted due to an API error: {e}]")
        break

    except Exception as e:
        interrupted = True
        print(f"\n[Streaming interrupted unexpectedly: {e}]")
        break

print()
full_text = "".join(collected_text)

if not collected_text:
    print("No response was generated.")
elif finish_reason not in ("STOP", None):
    print(f"[Incomplete response. Reason: {finish_reason}]")
elif interrupted:
    print("[Incomplete response.]")
else:
    # validating the structured response using the Pydantic model
    try:
        parsed = ExplanationResponse.model_validate_json(full_text)
        print("\n[Complete and valid response.]")
        print(f"\nExplanation: {parsed.explanation}")
        print(f"Analogy: {parsed.analogy}")
    except ValidationError as e:
        # printing the raw text too, so a failed validation is debuggable instead of just showing the Pydantic error with no context
        print(f"[Response rejected: output failed validation: {e}.]")
        print(f"\nRaw response: {full_text}")
