from models import build_model
import torch
import soundfile as sf
from kokoro import generate

def generate_and_save(model, text, voicepack, voice_name, output_name, lang='a'):
    print(f"\nGenerating: {output_name}")
    print(f"Text: {text}")
    audio, phonemes = generate(model, text, voicepack, lang=lang)
    output_file = f"output_{output_name}.wav"
    sf.write(output_file, audio, 24000)
    print(f"Audio saved to: {output_file}")
    print(f"Phonemes used: {phonemes}")

def main():
    # Initialize device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Build model
    model = build_model('kokoro-v0_19.pth', device)
    
    # Test different voices and speaking styles
    voices = {
        'default': 'af',      # 50-50 mix of Bella & Sarah
        'sarah': 'af_sarah',  # Female American
        'george': 'bm_george', # Male British
        'bella': 'af_bella',  # Female American
        'michael': 'am_michael'  # Male American
    }
    
    # Test different voices and styles
    tests = [
        {
            'voice': 'default',
            'text': "Hello! This is how the default voice sounds.",
            'name': 'default_voice'
        },
        {
            'voice': 'sarah',
            'text': "Hi there! I'm Sarah, and I speak with an American accent.",
            'name': 'sarah_voice'
        },
        {
            'voice': 'george',
            'text': "Good evening! I'm George, speaking with a British accent.",
            'name': 'george_voice',
            'lang': 'b'
        },
        {
            'voice': 'bella',
            'text': "Hey! I'm Bella, another American voice. Let me tell you a story!",
            'name': 'bella_voice'
        },
        {
            'voice': 'michael',
            'text': "Greetings! This is Michael, demonstrating a male American voice.",
            'name': 'michael_voice'
        }
    ]
    
    # Generate all test cases
    for test in tests:
        voice_name = test['voice']
        voicepack = torch.load(f'voices/{voices[voice_name]}.pt', weights_only=True).to(device)
        generate_and_save(
            model, 
            test['text'], 
            voicepack, 
            voice_name, 
            test['name'],
            test.get('lang', 'a')  # Default to American English
        )

if __name__ == "__main__":
    main()
