import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# loading .env file, so that we can read the API key
load_dotenv()

# creating the client using the key from environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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

# sending your prompt with system instruction
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction
    )
)

# printing the response from the model
print("\nGEMINI:")
print(response.text)