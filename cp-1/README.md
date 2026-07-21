# Checkpoint 1: LLM API Integration

## Overview
Basic integration with the Gemini API — sends a user-provided prompt
and prints the response.

## Features
- API key loaded securely from an environment variable (`.env`), never hardcoded in the source file
- Takes prompt input directly from the user

## Setup
1. Add your GEMINI_API_KEY to `.env`
2. `pip install google-genai python-dotenv`
3. `python main.py`