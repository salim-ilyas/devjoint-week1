# AI ENGINEERING Internship — Week 1

LLM-based implementation: API integration, prompt engineering,
streaming, error handling, output validation, and cost/token
awareness — built incrementally across 6 checkpoints using the
Gemini API.

## Checkpoints

- [Checkpoint 1: LLM API Integration](./cp-1) — basic Gemini API call
  with the key loaded securely from an environment variable
- [Checkpoint 2: Prompt Engineering](./cp-2) — structured system
  prompt with few-shot examples for consistent output format
- [Checkpoint 3: Streaming Response Management](./cp-3) — streams the
  response chunk-by-chunk instead of waiting for the full reply
- [Checkpoint 4: Error Handling](./cp-4) — retry logic for rate
  limits, timeouts, and general API errors
- [Checkpoint 5: Output Parsing / Validation](./cp-5) — switches to
  structured JSON output and validates it before use
- [Checkpoint 6: Cost / Token Awareness](./cp-6) — logs token usage
  (including thinking tokens) and estimates cost per request

## Tech Stack
- Python
- Gemini API (`google-genai`)
- `python-dotenv` for environment variable management