from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import torch

def generate_speech(text, output_path="output.wav"):
    """Generate speech from text using Bark."""
    # Preload models
    print("Loading models...")
    preload_models()
    
    # Set device
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    
    # Generate audio
    print(f"\nGenerating speech for text: {text}")
    audio_array = generate_audio(text, history_prompt="v2/en_speaker_6")
    
    # Save audio
    print(f"\nSaving audio to {output_path}")
    write_wav(output_path, SAMPLE_RATE, audio_array)
    
    return output_path

if __name__ == "__main__":
    # Test the model with a sample text
    test_text = """Hello, my name is Suno. And, uh — and I like pizza. [subtle laughter]  But I also have other interests such as playing tic tac toe."""
    
    output_file = generate_speech(test_text)
    print(f"\nDone! Audio saved to {output_file}")
