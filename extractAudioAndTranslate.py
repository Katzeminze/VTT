from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment

import whisper
import csv

from pydub import AudioSegment
import math
import os
from AzureTest import ChatBot


def transcribe_audio_with_whisper(audio_path, model_name="base"):
    # Load Whisper model
    model = whisper.load_model(model_name)
    # Transcribe audio
    result = model.transcribe(audio_path, language="de")
    return result["text"]

def save_to_csv(data, filename):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data])
        
def extract_audio_from_video(video_path, audio_path="extracted_audio.wav"):
    # Load the video file
    video = VideoFileClip(video_path)
    # Extract audio and save it
    video.audio.write_audiofile(audio_path)
    return audio_path

def segment_audio(file_path, segment_length=60000, output_folder="audio_segments"):
    """
    Segments an audio file into chunks.
    
    Parameters:
    - file_path (str): Path to the original audio file.
    - segment_length (int): Length of each segment in milliseconds. (e.g., 60000 ms = 1 minute)
    - output_folder (str): Folder to save the segmented audio files.

    Returns:
    - List of file paths for the audio segments.
    """
    # Load the audio file
    audio = AudioSegment.from_file(file_path)
    
    # Calculate the number of segments
    total_length = len(audio)
    num_segments = math.ceil(total_length / segment_length)
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    segment_paths = []
    for i in range(num_segments):
        # Calculate start and end times for each segment
        start_time = i * segment_length
        end_time = min((i + 1) * segment_length, total_length)
        
        # Extract segment
        segment = audio[start_time:end_time]
        
        # Export segment to file
        segment_path = os.path.join(output_folder, f"segment_{i+1}.wav")
        segment.export(segment_path, format="wav")
        segment_paths.append(segment_path)
    
    return segment_paths

def transcribe_audio(audio_path, language="de-DE"):
    recognizer = sr.Recognizer()
    # Load the audio file
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        # Recognize (convert from speech to text)
        try:
            text = recognizer.recognize_google(audio_data, language=language)
        except sr.UnknownValueError:
            text = "Could not understand audio"
        except sr.RequestError:
            text = "Could not request results; check your internet connection"
    return text

def extract_text_from_video(video_path):
    final_str = ''
    # Step 1: Extract audio from video
    audio_path = extract_audio_from_video(video_path)
    # # # Step 2: Segment audio to 1 minute
    segments = segment_audio(audio_path, segment_length=60000) # 60,000 ms = 1 minute
    # print("Segments:", segments)
    # Step 3: Transcribe the audio segment with Whisper
    for segment in segments:
        text = transcribe_audio_with_whisper(segment)
        # save_to_csv(text, "transcribed_text.csv")
    # text = transcribe_audio_with_whisper(audio_path)
    
        chat = ChatBot()
        response = chat.send_request_and_get_response(f"Translate the following into English: {text}?")
        # Handle the response as needed (e.g., print or process)
        data = response.json()
        print(data)
        content = data['choices'][0]['message']['content'] 
        final_str = final_str + content
    save_to_csv(final_str, "english_text.csv")

# Example usage
video_path = r"C:\Users\nyrobtseva\Documents\ToText_EN\nctable-issue-NCC-3466.mp4"  # Replace with your video file path
transcribed_text = extract_text_from_video(video_path)
# print("Transcribed Text:\n", transcribed_text)

# chat = ChatBot()
# response = chat.send_request_and_get_response(f"Translate the following into English: {transcribed_text}?")
# # Handle the response as needed (e.g., print or process)
# data = response.json()
# print(data)
# content = data['choices'][0]['message']['content']
# save_to_csv(content, "english_text.csv")
