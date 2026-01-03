# tetststst

## MLX-LM Text Generation

This repository contains a Python script and REST API server for generating text using MLX-LM with the OpenAI GPT OSS 20B model. The API allows global access to the model through HTTP endpoints.

### Files

- `generate_text.py`: Python script that loads the MLX model and generates text
- `api_server.py`: FastAPI server exposing MLX-LM via REST API endpoints
- `example_client.py`: Example client demonstrating how to use the API
- `.github/workflows/mlx-lm.yml`: GitHub Actions workflow to run the text generation
- `.github/workflows/mlx-lm-api.yml`: GitHub Actions workflow to run the API server
- `Dockerfile`: Docker configuration for containerized deployment
- `docker-compose.yml`: Docker Compose configuration for easy local setup
- `requirements.txt`: Python dependencies

### Quick Start

#### Option 1: Run the API Server Locally

**Prerequisites**: This requires Apple Silicon (M1/M2/M3) as MLX is optimized for Apple's hardware.

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
python api_server.py
```

The API will be available at `http://localhost:8000`
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

#### Option 2: Run with Docker

```bash
# Build and run with Docker Compose
docker-compose up

# Or build manually
docker build -t mlx-lm-api .
docker run -p 8000:8000 mlx-lm-api
```

#### Option 3: Run the Standalone Script

```bash
# Install dependencies
pip install mlx-lm

# Run the script
python generate_text.py
```

### Using the API

#### Available Endpoints

- `GET /` - API information and available endpoints
- `GET /health` - Health check endpoint
- `POST /generate` - Generate text from a prompt
- `POST /generate/chat` - Chat-optimized text generation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

#### Example API Request

```bash
# Using curl
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a story about Einstein",
    "max_tokens": 150,
    "temperature": 0.7,
    "verbose": true
  }'
```

```python
# Using Python requests
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={
        "prompt": "Write a story about Einstein",
        "max_tokens": 150,
        "temperature": 0.7
    }
)
result = response.json()
print(result["generated_text"])
```

#### Example Client

Run the included example client to see the API in action:

```bash
python example_client.py
```

This will demonstrate multiple examples of text generation with different prompts and parameters.

### API Parameters

- `prompt` (required): The text prompt for generation
- `max_tokens` (optional, default: 100): Maximum number of tokens to generate (1-2048)
- `temperature` (optional, default: 0.7): Sampling temperature (0.0-2.0)
  - Lower values (e.g., 0.3) make output more focused and deterministic
  - Higher values (e.g., 0.9) make output more creative and random
- `verbose` (optional, default: true): Whether to show verbose output during generation

### GitHub Actions Workflows

#### Text Generation Workflow

The workflow is configured to run on:
- Manual trigger (workflow_dispatch)
- Push to main/master branches
- Pull requests to main/master branches

#### API Server Workflow

The API server workflow can be triggered manually with:
- `port`: Port to run the server on (default: 8000)
- `duration`: How long to run the server in minutes (default: 30)

**Note**: Both workflows use `macos-latest` runners. For production use with actual Apple Silicon, you would need to configure self-hosted runners on macOS with Apple Silicon hardware.

### Deployment Options

#### Local Development
Best for testing and development on Apple Silicon machines.

#### Docker Deployment
Can be deployed to any platform, though performance will be optimal on Apple Silicon.

#### Cloud Deployment
Deploy to cloud platforms that support custom containers:
- AWS EC2 (with Mac instances for Apple Silicon)
- Google Cloud (with custom VM)
- Azure (with custom VM)
- Fly.io, Railway, or similar container platforms

### How It Works

The system:
1. Loads the `inferencerlabs/openai-gpt-oss-20b-MLX-6.5bit` model on startup
2. Exposes REST API endpoints for text generation
3. Accepts prompts via HTTP POST requests
4. Formats prompts as chat messages
5. Generates text using the MLX model
6. Returns generated text in JSON format

### Security Notes

- The API runs without authentication by default - add authentication for production use
- Consider rate limiting for public deployments
- Monitor resource usage as model inference can be resource-intensive
- Use HTTPS in production environments