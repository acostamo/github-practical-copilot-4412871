import os
import eyed3
import yaml

# Create a function that reads audio files in the mp3 format from
# the 'audio' directory and returns a list of them.
def get_audio_files():
    audio_files = []
    for file in os.listdir('audio'):
        if file.endswith('.mp3'):
            file_path = os.path.join('audio', file)
            # Append ID3 data of the audio file to the list
            audio_files.append(read_id3_data(file_path, file))
    return audio_files

# Create a function that reads ID3 data from the audio files
def read_id3_data(file_path, filename):
    # Load the audio file using eyed3
    audiofile = eyed3.load(file_path)
    
    # Get the duration of the audio file in seconds and format it as HH:MM:SS
    duration_secs = int(audiofile.info.time_secs)
    duration_formatted = f"{duration_secs // 3600:02}:{(duration_secs % 3600) // 60:02}:{duration_secs % 60:02}"
    
    # Get the size of the audio file in bytes and format it with commas
    file_size = os.path.getsize(file_path)
    file_size_formatted = f"{file_size:,}"
    
    # Create a dictionary with the ID3 data
    id3_data = {
        "file": 'audio/' + filename,  # File path
        "title": audiofile.tag.title,  # Title of the audio file
        "description": [comment.text for comment in audiofile.tag.comments],  # List of comments
        "duration": duration_formatted,  # Formatted duration
        "lenght": file_size_formatted  # Formatted file size
    }
    return id3_data

# Get the list of audio files with their ID3 data
audio_files = get_audio_files()

# Write the audio files data to a YAML file
with open('episodes.yaml', 'w') as file:
    yaml.dump(audio_files, file, default_flow_style=False, sort_keys=False)