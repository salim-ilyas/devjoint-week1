import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

# loading .env file, so that we can read the API key
load_dotenv()
# checking GEMINI_API_KEY exists before creating the client
api_key=os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("No API key found.")
# creating the client using the key from environment variable
client = genai.Client(api_key=api_key)

# setting the system instruction
system_instruction = ("""
You must respond with ONLY the following two lines. Do not add headers, bullet points, markdown formatting, numbered sections, or any additional information beyond these two lines:

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
Analogy: It's like water flowing through a pipe, powering anything it passes through.""")

prompt = input("Enter your prompt for Gemini: ")
print("Sending the prompt to Gemini...")

print("\nGEMINI:")

collected_text = []
finish_reason = None
interrupted = False

try:
    # sending your prompyt and streaming the response
    stream = client.models.generate_content_stream(
        model="gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
        )
    )

    for chunk in stream:
        # if a chunk has no candidates, it means the model hasn't generated any text yet, so we skip it
        if not chunk.candidates:
            continue
        candidate = chunk.candidates[0]

        # printing text as it streams in, flushing so it shows up immediately
        if chunk.text:
            print(chunk.text, end="", flush=True)
            collected_text.append(chunk.text)

        if candidate.finish_reason is not None:
            finish_reason = candidate.finish_reason

except KeyboardInterrupt:
    # if the user presses Ctrl+C, we want to stop streaming and print a message
    interrupted = True
    print("\n\n[Streaming interrupted by user].")

except genai_errors.APIError as e:
    # covers dropped connections, timeouts, and API errors
    interrupted = True
    print(f"\n\n[Streaming interrupted due to an API error: {e}]")

except Exception as e:
    # covers any other unexpected errors
    interrupted = True
    print(f"\n\n[Streaming interrupted unexpectedly: {e}]")

finally:
    print()
    if not collected_text:
        print("No response was generated.")
    elif interrupted:
        print("[Incomplete response.]")
    elif finish_reason not in ("STOP", None):
        print(f"[Incomplete response. Reason: {finish_reason}]")
    else:
        print("[Response complete.]")
