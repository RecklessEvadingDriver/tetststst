#!/usr/bin/env python3
"""
FastAPI server to expose MLX-LM text generation via REST API endpoints.
This allows the model to be accessed globally via HTTP requests.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
from mlx_lm import load, generate

app = FastAPI(
    title="MLX-LM Text Generation API",
    description="API for generating text using MLX-LM with OpenAI GPT OSS 20B model",
    version="1.0.0"
)

# Global variables for model and tokenizer
model = None
tokenizer = None

class GenerationRequest(BaseModel):
    """Request model for text generation."""
    prompt: str = Field(..., description="The text prompt for generation", min_length=1)
    max_tokens: Optional[int] = Field(100, description="Maximum number of tokens to generate", gt=0, le=2048)
    temperature: Optional[float] = Field(0.7, description="Sampling temperature", ge=0.0, le=2.0)
    verbose: Optional[bool] = Field(True, description="Whether to show verbose output")

class GenerationResponse(BaseModel):
    """Response model for text generation."""
    generated_text: str
    prompt: str
    model: str = "inferencerlabs/openai-gpt-oss-20b-MLX-6.5bit"

@app.on_event("startup")
async def load_model():
    """Load the MLX model and tokenizer on startup."""
    global model, tokenizer
    print("Loading MLX model...")
    model, tokenizer = load("inferencerlabs/openai-gpt-oss-20b-MLX-6.5bit")
    print("Model loaded successfully!")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "MLX-LM Text Generation API",
        "endpoints": {
            "/generate": "POST - Generate text from a prompt",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation (Swagger UI)",
            "/redoc": "GET - API documentation (ReDoc)"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/generate", response_model=GenerationResponse)
async def generate_text(request: GenerationRequest):
    """
    Generate text using the MLX-LM model.
    
    Args:
        request: GenerationRequest with prompt and generation parameters
    
    Returns:
        GenerationResponse with generated text
    """
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Format the prompt as a chat message
        messages = [{"role": "user", "content": request.prompt}]
        formatted_prompt = tokenizer.apply_chat_template(
            messages, add_generation_prompt=True
        )
        
        # Generate text
        generated = generate(
            model, 
            tokenizer, 
            prompt=formatted_prompt, 
            max_tokens=request.max_tokens,
            temp=request.temperature,
            verbose=request.verbose
        )
        
        return GenerationResponse(
            generated_text=generated,
            prompt=request.prompt
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/generate/chat")
async def generate_chat(request: GenerationRequest):
    """
    Alternative endpoint specifically formatted for chat-style interactions.
    Uses the same generation logic but with chat-optimized formatting.
    """
    return await generate_text(request)

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "api_server:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=False,
        log_level="info"
    )
