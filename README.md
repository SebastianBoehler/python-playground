# Python Playground

This repository contains various Python projects and experiments with AI and multimedia processing.

## Project Structure

### `/apps`
- **shortVideos/**: Application that generates short-form videos with AI
  - Uses Gemini for story generation
  - OuteTTS for text-to-speech conversion
  - Whisper for speech-to-text with timestamps
  - MoviePy for video editing and text overlay
  - Requirements and environment variables managed in `requirements.txt` and `.env`

### `/stt` (Speech-to-Text)
- **whisper-l-v3-turbo/**: Implementation using OpenAI's Whisper Large V3 Turbo model
  - High-accuracy transcription with timestamp support
  - Optimized for both CPU and GPU usage

### `/tts` (Text-to-Speech)
- **bark/**: Experiments with Bark text-to-speech model
  - (In development)

## Setup and Installation

Each project has its own `requirements.txt` file for managing dependencies. To set up a project:

1. Navigate to the project directory
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Environment Variables

Some projects require environment variables to be set:
- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
- `GOOGLE_CLOUD_LOCATION`: Google Cloud region (e.g., "us-central1")
