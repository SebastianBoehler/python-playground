from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from models import build_model
from kokoro import generate
import soundfile as sf
import io
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize device and model globally
device = 'cuda' if torch.cuda.is_available() else 'cpu'
logger.info(f"Using device: {device}")

logger.info("Loading model...")
model = build_model('kokoro-v0_19.pth', device)
logger.info("Model loaded successfully")

# Voice mappings
VOICES = {
    'default': 'af',      # 50-50 mix of Bella & Sarah
    'sarah': 'af_sarah',  # Female American
    'george': 'bm_george', # Male British
    'bella': 'af_bella',  # Female American
    'michael': 'am_michael'  # Male American
}

# Load voice packs globally
logger.info("Loading voice packs...")
VOICE_PACKS = {}
for voice_name, voice_id in VOICES.items():
    try:
        logger.info(f"Loading voice pack: {voice_name} ({voice_id})")
        VOICE_PACKS[voice_name] = torch.load(f'voices/{voice_id}.pt', map_location=device).to(device)
    except Exception as e:
        logger.error(f"Error loading voice pack {voice_name}: {str(e)}")
logger.info("Voice packs loaded successfully")

class TTSRequest(BaseModel):
    text: str
    voice: str = "default"  # default voice
    language: str = "a"  # default language

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    try:
        logger.info(f"Received TTS request - Voice: {request.voice}, Text: {request.text}")
        
        # Get voice pack
        if request.voice not in VOICE_PACKS:
            logger.error(f"Voice '{request.voice}' not found")
            raise HTTPException(status_code=400, detail=f"Voice '{request.voice}' not found. Available voices: {list(VOICES.keys())}")
        
        voicepack = VOICE_PACKS[request.voice]
        logger.info("Voice pack loaded")
        
        # Generate audio
        logger.info("Generating audio...")
        audio, phonemes = generate(model, request.text, voicepack, lang=request.language)
        logger.info(f"Audio generated successfully. Phonemes: {phonemes}")
        
        # Save to bytes buffer
        logger.info("Converting to WAV format...")
        buffer = io.BytesIO()
        sf.write(buffer, audio, 24000, format='WAV')
        buffer.seek(0)
        
        # Convert to base64
        logger.info("Converting to base64...")
        audio_base64 = base64.b64encode(buffer.read()).decode()
        logger.info("Conversion complete")
        
        return {
            "status": "success",
            "audio": audio_base64,
            "phonemes": phonemes
        }
    except Exception as e:
        logger.error(f"Error in TTS endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/voices")
async def list_voices():
    return {
        name: {
            "id": voice_id,
            "description": "Female American" if "af_" in voice_id else
                         "Male British" if "bm_" in voice_id else
                         "Male American" if "am_" in voice_id else
                         "50-50 mix of Bella & Sarah"
        }
        for name, voice_id in VOICES.items()
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

# Add CORS middleware to allow web UI to access the API
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
