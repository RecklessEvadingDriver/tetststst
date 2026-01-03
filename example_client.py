#!/usr/bin/env python3
"""
Example client to demonstrate using the MLX-LM API endpoints.
This can be run from anywhere to interact with the API.
"""

import requests
import json
import sys

# API endpoint - change this to your deployed server URL
API_URL = "http://localhost:8000"

def check_health():
    """Check if the API server is healthy."""
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        print("✓ API server is healthy!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ API server is not reachable: {e}")
        return False

def generate_text(prompt, max_tokens=100, temperature=0.7, verbose=True):
    """
    Generate text using the MLX-LM API.
    
    Args:
        prompt: The text prompt for generation
        max_tokens: Maximum number of tokens to generate
        temperature: Sampling temperature (0.0 to 2.0)
        verbose: Whether to show verbose output
    
    Returns:
        Generated text or None if failed
    """
    try:
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "verbose": verbose
        }
        
        print(f"\nSending request to: {API_URL}/generate")
        print(f"Prompt: {prompt}")
        print(f"Parameters: max_tokens={max_tokens}, temperature={temperature}")
        print("\nGenerating...")
        
        response = requests.post(
            f"{API_URL}/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        result = response.json()
        print("\n" + "="*80)
        print("GENERATED TEXT:")
        print("="*80)
        print(result["generated_text"])
        print("="*80)
        
        return result["generated_text"]
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        if hasattr(e.response, 'text'):
            print(f"Error details: {e.response.text}")
        return None

def main():
    """Main function to demonstrate API usage."""
    print("MLX-LM API Client")
    print("="*80)
    
    # Check if API is available
    if not check_health():
        print("\nMake sure the API server is running:")
        print("  Local: python api_server.py")
        print("  Docker: docker-compose up")
        sys.exit(1)
    
    # Example 1: Generate a story about Einstein
    print("\n\nExample 1: Story about Einstein")
    print("-"*80)
    generate_text(
        prompt="Write a story about Einstein",
        max_tokens=150,
        temperature=0.7
    )
    
    # Example 2: Technical explanation
    print("\n\nExample 2: Technical explanation")
    print("-"*80)
    generate_text(
        prompt="Explain quantum computing in simple terms",
        max_tokens=100,
        temperature=0.5
    )
    
    # Example 3: Creative writing
    print("\n\nExample 3: Creative writing")
    print("-"*80)
    generate_text(
        prompt="Write a haiku about artificial intelligence",
        max_tokens=50,
        temperature=0.9
    )

if __name__ == "__main__":
    main()
