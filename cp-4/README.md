# Checkpoint 4: Error Handling

## Overview
Adds retry logic and error handling around the Gemini API call, so the
program responds gracefully to common failure cases instead of crashing.

## Errors Handled

### 1. Rate Limit / Quota Errors (HTTP 429 — RESOURCE_EXHAUSTED)
Occurs when too many requests are sent within the allowed time window
(Gemini's free tier allows a limited number of requests per day/minute).

**Handling:** The program catches this specific error, waits a short
delay, and automatically retries the request — up to 3 attempts, with
the wait time increasing on each retry (5s, 10s, 15s).

### 2. Other API/Client Errors
Any other error returned directly by the Gemini API (e.g. invalid
request, authentication issues) that isn't a rate limit.

**Handling:** Caught separately, prints a clear error message, and
stops — since retrying wouldn't fix a non-rate-limit issue.

### 3. Timeout Errors
Occurs if the API takes too long to respond (e.g. network issues).

**Handling:** A 10-second timeout is set on the request. If exceeded,
the program catches it and retries, same as other transient errors.

### 4. Unexpected Errors
Any error not related to the API itself (e.g. network issues, unexpected
bugs).

**Handling:** Caught with a general exception handler so the program
exits cleanly with a readable message instead of a raw traceback.

### 5. Max Retries Exceeded
If all 3 retry attempts fail, the program stops and informs the user
to try again later, rather than retrying indefinitely.