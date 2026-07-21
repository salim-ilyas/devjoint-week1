# Checkpoint 5: Output Parsing / Validation

## Overview
Switches the model's output from plain text to structured JSON, and
validates the response before using it — catching cases where the
output is malformed or missing expected fields.

## Features
- System prompt instructs the model to respond with JSON only
(`explanation` and `analogy` fields)
- Response is streamed and collected into a single string
- Cleans up common formatting issues (e.g. markdown code fences like
\`\`\`json ... \`\`\`) before parsing
- Attempts to parse the response with `json.loads()` — catches
`JSONDecodeError` if the output is not valid JSON
- Checks that required fields (`explanation`, `analogy`) are present
even if the JSON itself is valid
- If validation fails at any step, the program reports a clear error
instead of crashing or using bad data

## Setup
1. Add your GEMINI_API_KEY to `.env`
2. `pip install google-genai python-dotenv`
3. `python main.py`