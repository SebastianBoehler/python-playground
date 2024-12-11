import os
import vertexai
from vertexai.generative_models import GenerativeModel
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datetime import datetime
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import numpy as np

class ShortVideoGenerator:
    def __init__(self):
        # Initialize Gemini
        vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), 
                     location=os.getenv("GOOGLE_CLOUD_LOCATION"))
        self.story_model = GenerativeModel(
            "gemini-1.5-flash-002",
            system_instruction=["""
                Create a story, starting with a catching hook. Output the story in a way that it can be directly read out.
                Use the hook to hook the listeners into the topic.
                The story should be 1-2 paragraphs long and have a surprising twist at the end.
                Keep it concise but impactful.
                **Do not use headers, title etc, Output the script in a way that it can be directly read out, without instructions.**
                Write in first person. use slang and humor.
                **IMPORTANT** Use \n after each sentence.

                Use [nervous laughter] or [stutter] to indicate character emotion.
                **Important use [] brackets to indicate character emotion.**

                Example: 
                I recently ran into my ex girlfriend - uhm. She told me that she got gay after we had sex for the first time. [nervous laughter]
            """]
        )
        
        # Initialize Bark TTS
        preload_models()
        
        # Initialize Whisper
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        model_id = "openai/whisper-large-v3-turbo"
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(device)
        
        processor = AutoProcessor.from_pretrained(model_id)
        
        self.whisper_pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
        )
    
    def generate_story(self, theme):
        """Generate a short story with a hook."""
        prompt = f"""Create a short, engaging story with a powerful hook about {theme}."""
        
        response = self.story_model.generate_content(prompt)
        return response.text
    
    # can only take in a string of certain length, otherwise exceeds the max audio time output
    def create_speech(self, text):
        """Convert text to speech using Bark TTS."""
        # Split text into sentences using newlines
        sentences = [s.strip() for s in text.split('\n') if s.strip()]
        
        # Generate audio for each sentence
        audio_arrays = []
        for sentence in sentences:
            if sentence:
                # Generate audio from text
                audio_array = generate_audio(sentence)
                audio_arrays.append(audio_array)
        
        # Concatenate all audio arrays
        combined_audio = np.concatenate(audio_arrays)
        
        # Save to a file
        audio_path = "speech.wav"
        write_wav(audio_path, SAMPLE_RATE, combined_audio)
        return audio_path
    
    def transcribe_with_timestamps(self, audio_path):
        """Transcribe audio to text with timestamps using Whisper."""
        generate_kwargs = {
            # "max_new_tokens": 448,
            "language": "english",
            "task": "transcribe",
            "temperature": 0.5,
        }
        result = self.whisper_pipe(audio_path, return_timestamps="word", generate_kwargs=generate_kwargs) # timestamps on word level
        # returns result["chunks"]
        return result
    
    def overlay_text_on_video(self, video_path, transcription, audio_path):
        """Overlay transcribed text on video at corresponding timestamps."""
        print("\n4. Creating video with text overlay and audio...")
        
        # Load the video and audio
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        # Create text clips for each transcribed chunk
        text_clips = []
        for chunk in transcription["chunks"]:
            text = chunk["text"]
            start_time, end_time = chunk["timestamp"]
            duration = end_time - start_time
            
            # Create text clip with styling - using doc example format
            txt_clip = (TextClip(
                text=text,
                font_size=70,
                color='white',
                font="/System/Library/Fonts/Helvetica.ttc"  # Using system font on macOS
            ).with_duration(duration)
             .with_position(('center', 'bottom'))
             .with_start(start_time))
            
            text_clips.append(txt_clip)
        
        # Combine video with text overlays and audio
        final_video = CompositeVideoClip([video] + text_clips)
        final_video = final_video.with_audio(audio)
        
        # Write the result
        output_path = "output_video.mp4"
        final_video.write_videofile(output_path, 
                                  codec='libx264', 
                                  audio_codec='aac',
                                  fps=24)
        
        # Clean up
        video.close()
        final_video.close()
        
        return output_path
    
    def generate_full_video_content(self, theme):
        """Generate complete video content: story, speech, and transcription."""
        # Step 1: Generate the story
        print("1. Generating story...")
        story = self.generate_story(theme)
        print("\nGenerated Story:")
        print(story)
        
        # Step 2: Convert to speech
        print("\n2. Converting to speech...")
        audio_path = self.create_speech(story)
        print(f"Speech saved to: {audio_path}")
        
        # Step 3: Transcribe with timestamps
        print("\n3. Transcribing speech...")
        transcription = self.transcribe_with_timestamps(audio_path)
        
        print("\nTranscription with timestamps:")
        for chunk in transcription["chunks"]:
            print(chunk)  # {'text': ' they', 'timestamp': (0.0, 0.28)}
        
        # Step 4: Create video with text overlay and audio
        source_video_path = os.path.join("sourceVids", "video.mov")
        output_video_path = self.overlay_text_on_video(source_video_path, transcription, audio_path)
        print(f"\nVideo with overlay and audio saved to: {output_video_path}")
        
        return {
            "story": story,
            "audio_path": audio_path,
            "transcription": transcription,
            "video_path": output_video_path
        }

if __name__ == "__main__":
    generator = ShortVideoGenerator()
    result = generator.generate_full_video_content("create a story from a person eating its cat by mistake")
