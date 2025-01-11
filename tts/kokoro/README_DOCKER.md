# Kokoro TTS Docker Server

This is a Docker container that provides a web interface and API for the [Kokoro TTS model](https://huggingface.co/hexgrad/Kokoro-82M). This Docker implementation is a wrapper around the original model to make it easier to use in production environments.

## Attribution

- Original Kokoro TTS Model: [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- This Docker implementation wraps the original model with a FastAPI server and web interface

## Features

- Web-based interface for easy text-to-speech conversion
- RESTful API for programmatic access
- Multiple voice options:
  - Default (50-50 mix of Bella & Sarah)
  - Sarah (Female American)
  - George (Male British)
  - Bella (Female American)
  - Michael (Male American)
- Real-time audio generation and playback
- Phoneme visualization

## Docker Hub

The image is available on Docker Hub:

```bash
docker pull sebastianboehler/kokoro-tts
```

## Running Locally

If you want to build and run the container locally:

```bash
# Build the image
docker build -t kokoro-tts .

# Run the container
docker run -p 8000:8000 kokoro-tts
```

The server will be available at http://localhost:8000

## API Endpoints

### 1. Generate Speech (/tts)
POST request with JSON body:
```json
{
    "text": "Hello, how are you?",
    "voice": "af",  // optional, defaults to "af"
    "language": "a" // optional, defaults to "a"
}
```

### 2. List Available Voices (/voices)
GET request to see all available voices

### 3. Health Check (/health)
GET request to check server status

## Example Usage with curl

```bash
# Generate speech
curl -X POST "http://localhost:8000/tts" \
     -H "Content-Type: application/json" \
     -d '{"text":"Hello, how are you?","voice":"sarah"}'

# List voices
curl "http://localhost:8000/voices"

# Health check
curl "http://localhost:8000/health"
```

## License

This Docker implementation is provided under the MIT License. However, please note that the original Kokoro TTS model has its own license and terms of use. Make sure to check and comply with the original model's license at [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
