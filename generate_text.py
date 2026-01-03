#!/usr/bin/env python3
"""
Generate text using MLX-LM with the openai-gpt-oss-20b model.
"""

from mlx_lm import load, generate

# Load the model and tokenizer
model, tokenizer = load("inferencerlabs/openai-gpt-oss-20b-MLX-6.5bit")

# Define the prompt
prompt = "Write a story about Einstein"
messages = [{"role": "user", "content": prompt}]
prompt = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True
)

# Generate text
text = generate(model, tokenizer, prompt=prompt, verbose=True)
