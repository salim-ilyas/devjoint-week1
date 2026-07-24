import os
from dotenv import load_dotenv
from google import genai

# loading .env file, so that we can read the API key
load_dotenv()
# checking GEMINI_API_KEY exists before creating the client
api_key=os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("No API key found.")
# creating the client using the key from environment variable
client = genai.Client(api_key=api_key)

prompt = input("Enter your prompt for Gemini: ")
print("Sending the prompt to Gemini...")
# sending your prompt
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt
)
# handling empty, blocked, or interrupted responses
if not response.candidates:
    print("\nNo response was generated.")
elif response.candidates[0].finish_reason not in ("STOP", None):
    print(f"\nIncomplete response. Reason: {response.candidates[0].finish_reason}")
elif not response.text:
    print("\nGemini returned an empty response.")
else:
    print("\nGEMINI:")
    print(response.text) # printing the response from the model
