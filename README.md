# Python Playground

This repository contains various Python projects and experiments with AI and multimedia processing.

## Project Structure

### `/apps`
- **shortVideos/**: Application that generates short-form videos with AI
  - Uses Gemini 1.5 Flash for story generation with emotional markers and natural speech patterns
  - Bark TTS for high-quality text-to-speech conversion with emotional expressions
  - Whisper Large V3 Turbo for speech-to-text with timestamps
  - MoviePy for video editing and text overlay
  - Requirements and environment variables managed in `requirements.txt` and `.env`

### `/stt` (Speech-to-Text)
- **whisper-l-v3-turbo/**: Implementation using OpenAI's Whisper Large V3 Turbo model
  - High-accuracy transcription with timestamp support
  - Optimized for both CPU and GPU usage with `low_cpu_mem_usage=True`
  - Uses safetensors for efficient model loading

### `/tts` (Text-to-Speech)
- **bark/**: Implementation using Suno's Bark text-to-speech model
  - High-quality, natural-sounding speech synthesis
  - Support for emotional expressions ([nervous laughter], [sighs], etc.)
  - Voice customization using history prompts (e.g., "v2/en_speaker_6")
  - Sentence-by-sentence processing for handling long texts
  - Sample rate: 24kHz
- **outetts/**: Previous implementation using OuteTTS model
  - Basic text-to-speech capabilities
  - Speaker profile customization
  - Fixed voice characteristics
  - (Deprecated in favor of Bark TTS)

## Setup and Installation

Each project has its own `requirements.txt` file for managing dependencies. To set up a project:

1. Navigate to the project directory
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate the environment: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Environment Variables

Some projects require environment variables to be set:
- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
- `GOOGLE_CLOUD_LOCATION`: Google Cloud region (e.g., "us-central1")

## Models and Features

### Gemini 1.5 Flash
- Used for story generation
- Configured for first-person narratives with slang and humor
- Supports line breaks after each sentence for better TTS processing
- Includes emotional markers and natural speech patterns

### Bark TTS
- High-quality speech synthesis
- Voice customization via history prompts
- Supports emotional expressions in square brackets
- Processes text sentence by sentence for better handling of long content
- Default sample rate: 24kHz

### Whisper Large V3 Turbo
- Latest version of OpenAI's speech recognition model
- Memory-optimized loading with `low_cpu_mem_usage=True`
- Uses safetensors for efficient model storage
- Supports accurate timestamp generation

### OuteTTS (Deprecated)
- Basic text-to-speech synthesis
- Support for multiple speaker profiles
- Fixed voice characteristics per speaker
- Limited to ~25 seconds of audio per generation
- Replaced by Bark TTS for better quality and emotional expression
