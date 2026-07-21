# Checkpoint 6: Cost / Token Awareness

## Overview
Logs token usage and estimates cost per request, including thinking
tokens — which are billed at output rates but don't appear in the
visible response text, making them easy to miss.

## Features
- Pulls `prompt_token_count`, `candidates_token_count`, and
  `thoughts_token_count` from the API's `usage_metadata`
- Calculates estimated cost using per-token pricing for the model in
  use (gemini-flash-latest, currently Gemini 3.5 Flash: $0.75/M input,
  $4.50/M output — verify current rates at ai.google.dev/pricing, as
  Google updates these periodically)
- Thinking tokens are included in the