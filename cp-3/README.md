# Checkpoint 3: Streaming Response Management

## Overview
Streams the Gemini response chunk-by-chunk instead of waiting for the
full response, so text appears gradually as it's generated — similar
to how ChatGPT/Gemini's own interface displays responses.

## Features
- Uses `generate_content_stream` instead of `generate_content`
- Each chunk is printed immediately as it arrives (`flush=True`)
- Small delay added between chunks for smoother, more readable output

## Setup
1. Add your GEMINI_API_KEY to `.env`
2. `pip install google-genai python-dotenv`
3. `python main.py`