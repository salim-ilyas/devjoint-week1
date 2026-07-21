# Checkpoint 2: Prompt Engineering

## Overview
Adds a structured system prompt with few-shot examples on top of
checkpoint 1, so the model consistently responds in a fixed
"Explanation/Analogy" format regardless of the topic.

## Features
- System prompt separate from the user's question, defining the
model's behavior and required output format
- Three few-shot examples demonstrating the exact input → output
pattern expected
- User prompt still taken as free-form input