import os
from dotenv import load_dotenv
from google import genai

#Loading .env file, so that we can read the API key
load_dotenv()

#Creating the client using the key from environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
prompt = input("Enter your prompt for Gemini: ")
print("Sending the prompt to Gemini...")
#Sending your prompt
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt
)
#Printing the response from the model
print("\nGEMINI:")
print(response.text)