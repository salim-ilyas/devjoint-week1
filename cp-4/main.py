import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time
from google.genai import errors

# loading .env file, so that we can read the API key
load_dotenv()

# creating the client using the key from environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# setting the system instruction
system_instruction = """You must respond with ONLY the following two lines. Do not add headers, bullet points, markdown formatting, numbered sections, or any additional information beyond these two lines:

Explanation: <a simple 2-3 sentence explanation>
Analogy: <a short, relatable analogy>

Example 1:
User: What is gravity?
Explanation: Gravity is a force that pulls objects toward each other. On Earth, it pulls everything toward the ground.
Analogy: It's like an invisible magnet between Earth and everything on it.

Example 2:
User: What is an API?
Explanation: An API lets two computer programs talk to each other and exchange information.
Analogy: It's like a waiter taking your order to the kitchen and bringing back your food.

Example 3:
User: What is electricity?
Explanation: Electricity is the flow of tiny particles called electrons through a wire, which powers devices.
Analogy: It's like water flowing through a pipe, powering anything it passes through."""

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
            print("GEMINI:")
            for chunk in stream:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    time.sleep(0.05)
            print()
            return
        
        except errors.ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                wait_time = 5 * attempt  # waiting longer each retry
                print(f"\n[Rate limit hit. Retrying in {wait_time}s ({attempt} out of {max_retries} retries)]")
                time.sleep(wait_time)
            else:
                print(f"\n[API error: {e}]")
                return
            
        except Exception as e:
            print(f"\n[Unexpected error: {e}]")
            return
        
        except TimeoutError:
            print(f"\n[Request timed out. Retrying... ({attempt} out of {max_retries} retries)]")
            time.sleep(3)
    print("\n[Failed after max retries. Please try again later.]")

call_gemini_with_retry(prompt)