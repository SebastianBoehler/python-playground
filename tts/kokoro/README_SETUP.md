# Kokoro TTS Setup Guide

This guide will help you set up and run the Kokoro Text-to-Speech system on your machine.

## Prerequisites

- Python 3.8 or higher
- Git LFS (Large File Storage)
- espeak-ng
- Virtual environment (recommended)

## Installation Steps

1. **Install Git LFS**
```bash
brew install git-lfs
git lfs install
```

2. **Install espeak-ng**
```bash
brew install espeak-ng
```

3. **Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Unix/macOS
```

4. **Install Python dependencies**
Create a `requirements.txt` file with the following content:
```
phonemizer
torch
transformers
scipy
munch
soundfile
```

Then install the requirements:
```bash
pip install -r requirements.txt
```

## Usage Example

Here's a basic example of how to use Kokoro TTS:

```python
from models import build_model
import torch
import soundfile as sf
from kokoro import generate

# Initialize device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Build model and load default voice
model = build_model('kokoro-v0_19.pth', device)
voice_name = 'af'  # Default voice (Bella & Sarah mix)
voicepack = torch.load(f'voices/{voice_name}.pt', weights_only=True).to(device)

# Generate speech
text = "Hello! This is a test of the Kokoro text to speech system."
audio, phonemes = generate(model, text, voicepack, lang='a')  # 'a' for American English

# Save the audio
sf.write("output.wav", audio, 24000)  # 24kHz sample rate
```

## Available Voices

The system comes with several pre-trained voices:

| Voice Name | File Name | Description |
|------------|-----------|-------------|
| Default    | af        | 50-50 mix of Bella & Sarah |
| Bella      | af_bella  | Female American English |
| Sarah      | af_sarah  | Female American English |
| Adam       | am_adam   | Male American English |
| Michael    | am_michael| Male American English |
| Emma       | bf_emma   | Female British English |
| Isabella   | bf_isabella| Female British English |
| George     | bm_george | Male British English |
| Lewis      | bm_lewis  | Male British English |
| Nicole     | af_nicole | Female American English |
| Sky        | af_sky    | Female American English |

Note: The first letter in the voice file name indicates the accent:
- 'a' = American English
- 'b' = British English

The second letter indicates gender:
- 'f' = Female
- 'm' = Male

## Language Settings

When generating speech, use the appropriate language code:
- For American English voices: `lang='a'`
- For British English voices: `lang='b'`

## Troubleshooting

1. If you see warnings about `weight_norm` deprecation, these can be safely ignored as they don't affect functionality.

2. If you get errors about missing voices or model files, ensure that:
   - All voice files are in the `voices/` directory
   - The model file `kokoro-v0_19.pth` is in the root directory

3. If you get phonemizer errors, make sure espeak-ng is properly installed and accessible from your PATH.

## File Structure
```
kokoro/
├── models.py           # Model architecture definitions
├── kokoro.py          # Main TTS functionality
├── kokoro-v0_19.pth   # Pre-trained model weights
├── voices/            # Directory containing voice files
│   ├── af.pt
│   ├── af_bella.pt
│   └── ...
└── requirements.txt   # Python dependencies
```

## Credits

This implementation uses the Kokoro TTS model from [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M).
