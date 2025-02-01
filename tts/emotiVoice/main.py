import requests

# URL for the OpenAI-compatible TTS API
api_url = "http://localhost:8000/v1/audio/speech"

# Define the payload according to the SpeechRequest model
payload = {
    "input": "I'm absolutely thrilled to share this exciting news with you! We've just made a breakthrough in our research, and the results are far better than we could have ever imagined. The possibilities this opens up for future development are simply incredible.",
    "voice": "8051",
    "prompt": "Happy",
    "language": "English",
    "model": "emoti-voice",
    "response_format": "wav",
    "speed": 1.0
}

# Send a POST request to the TTS API endpoint
response = requests.post(api_url, json=payload)

# Check for a successful response
if response.status_code == 200:
    # Save the returned audio content
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("Audio saved to output.wav")
else:
    print(f"Error {response.status_code}: {response.text}")
