# EmotiVoice Integration

This folder contains the integration code for EmotiVoice, an advanced open-source text-to-speech engine with fine-grained emotional control.

## Prerequisites

- Docker installed
- NVIDIA GPU (required for the EmotiVoice container)
- NVIDIA Container Toolkit set up for Linux or Windows WSL2
- Python 3.8 or higher
- Virtual environment (recommended)

## Setup Instructions

1. **Start the EmotiVoice Docker Container**

   Make sure to run the container with both ports exposed (8501 for Streamlit interface and 8000 for the API):
   ```bash
   docker run -dp 127.0.0.1:8501:8501 -p 127.0.0.1:8000:8000 syq163/emoti-voice:latest
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Required Python Packages**
   ```bash
   pip install requests
   ```

## Usage

The `main.py` script demonstrates how to use the EmotiVoice API. It sends a text-to-speech request and saves the generated audio as a WAV file.

Key parameters in the request:
- `input`: The text to convert to speech
- `voice`: Speaker ID (default: "8051")
- `prompt`: Emotion or style (e.g., "Happy", "Sad", "Angry")
- `language`: Language code ("en" for English)
- `response_format`: Output audio format ("wav" or "mp3")
- `speed`: Speech speed multiplier (default: 1.0)

Example usage:
```python
import requests

api_url = "http://localhost:8000/v1/audio/speech"
payload = {
    "input": "Hello, I am feeling very happy today!",
    "voice": "8051",
    "prompt": "Happy",
    "language": "en",
    "model": "emoti-voice",
    "response_format": "wav",
    "speed": 1.0
}

response = requests.post(api_url, json=payload)
if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
```

## Accessing the Web Interface

You can also access the EmotiVoice web interface at http://localhost:8501 to experiment with different voices and emotions through a user-friendly interface.

## Troubleshooting

1. If you get connection errors, make sure:
   - The Docker container is running (`docker ps`)
   - Both ports (8501 and 8000) are properly exposed
   - You're using the correct API endpoint (/v1/audio/speech)

2. If you get audio generation errors:
   - Verify the payload structure matches the example above
   - Check that the voice ID exists
   - Ensure the text input is not empty
