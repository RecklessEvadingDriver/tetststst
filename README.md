# tetststst

## MLX-LM Text Generation

This repository contains a Python script that uses MLX-LM to generate text using the OpenAI GPT OSS 20B model.

### Files

- `generate_text.py`: Python script that loads the MLX model and generates text
- `.github/workflows/mlx-lm.yml`: GitHub Actions workflow to run the text generation
- `requirements.txt`: Python dependencies

### Running Locally

**Prerequisites**: This requires Apple Silicon (M1/M2/M3) as MLX is optimized for Apple's hardware.

```bash
# Install dependencies
pip install --upgrade mlx-lm

# Run the script
python generate_text.py
```

### GitHub Actions Workflow

The workflow is configured to run on:
- Manual trigger (workflow_dispatch)
- Push to main/master branches
- Pull requests to main/master branches

**Note**: The workflow uses `macos-latest` runners. For production use with actual Apple Silicon, you would need to configure self-hosted runners on macOS with Apple Silicon hardware.

### How It Works

The script:
1. Loads the `inferencerlabs/openai-gpt-oss-20b-MLX-6.5bit` model
2. Creates a chat prompt asking to "Write a story about Einstein"
3. Generates text using the model with verbose output